import logging
from typing import Optional

from fastapi import Request, APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .chat_history_db import ChatSession, Message, get_db
from .utils_api import *

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str
    system_message: str
    session_id: Optional[str] = None
    clear_history: bool = False


@router.get("/")
def read_root():
    return {"message": "Chat API is running. Use POST /chat endpoint."}


@router.post("/chat")
def chat(req: ChatRequest, request: Request, db: Session = Depends(get_db)):
    """Handle chat requests by generating a response from the LLaMA model.
    Note that `request` is generated by FastAPI for internal representation for backend. (Not sent by the client)
    """
    llm = request.app.state.llm
    logger.debug(f"Using LLM of type: {type(llm)}")

    session_id, db_session = get_or_create_session(db, req.session_id)

    system_message = req.system_message
    logger.debug(f"Using system message: {system_message[:50]}...")

    # Clear history if requested
    if req.clear_history:
        clear_session_history(db, session_id)
        return {"response": "History has been cleared!", "session_id": session_id}

    # Get history for this session
    db_messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.timestamp)
        .all()
    )

    # Build messages list
    # Format for Llama 3.2 is OpenAI chat format
    messages = [
        {"role": "system", "content": system_message},
    ]
    [messages.append({"role": msg.role, "content": msg.content}) for msg in db_messages]

    # Add the new user message
    num_new_msg_tokens, num_sys_token, num_sys_msg_token = validate_token_limits(
        llm, system_message, req.prompt
    )
    messages.append({"role": "user", "content": req.prompt})
    logger.debug(f"Sending {len(messages)} messages to LLM")

    # NOTE: change max_tokens and stop parameters depending on your use-case
    # Output
    output = llm.create_chat_completion(
        messages=messages, max_tokens=1000, temperature=1, repeat_penalty=1.2
    )
    logger.debug(f"Finish reason: {output['choices'][0]['finish_reason']}")
    response_text = output["choices"][0]["message"]["content"].strip()
    num_response_tokens = output["usage"]["completion_tokens"]
    num_total_tokens = output["usage"]["total_tokens"]

    trim_history_if_needed(db, db_messages, num_total_tokens, num_sys_token)

    save_conversation(
        db,
        session_id,
        req.prompt,
        response_text,
        num_new_msg_tokens,
        num_response_tokens,
    )
    return {"response": response_text, "session_id": session_id}


@router.get("/sessions")
def list_sessions(db: Session = Depends(get_db)):
    """List all available chat sessions."""
    sessions = db.query(ChatSession).all()
    result = []

    for session in sessions:
        message_count = (
            db.query(Message).filter(Message.session_id == session.session_id).count()
        )
        result.append(
            {
                "session_id": session.session_id,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "message_count": message_count,
            }
        )

    return {"sessions": result}


@router.get("/sessions/{session_id}")
def get_session(session_id: str, db: Session = Depends(get_db)):
    """Get a specific chat session's messages."""
    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.timestamp)
        .all()
    )

    return {
        "session_id": session_id,
        "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
    }


@router.delete("/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a chat session."""
    session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
        return {"status": "success", "message": f"Session {session_id} deleted"}
    return {"status": "error", "message": "Session not found"}
