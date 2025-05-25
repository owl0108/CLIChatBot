import uuid
from typing import Tuple, List, Optional
import logging
import datetime

from sqlalchemy.orm import Session
from llama_cpp import Llama
from .chat_history_db import ChatSession, Message
from .model import MAX_TOKENS

logger = logging.getLogger(__name__)


def get_or_create_session(
    db: Session, session_id: Optional[str] = None
) -> Tuple[str, ChatSession]:
    """Get an existing session or create a new one."""
    if not session_id:
        session_id = str(uuid.uuid4())

    db_session = (
        db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    )
    if not db_session:
        db_session = ChatSession(session_id=session_id)
        db.add(db_session)
        db.commit()
        logger.info(f"Created session for ID: {session_id}")

    return session_id, db_session


def clear_session_history(db: Session, session_id: str) -> None:
    """Clear all messages for a given session."""
    db.query(Message).filter(Message.session_id == session_id).delete()
    db.commit()
    logger.info(f"Cleared history for session {session_id}")


def validate_token_limits(
    llm: Llama, system_message: str, prompt: str
) -> Tuple[int, int, int]:
    """Validate that messages are within token limits and return token counts."""
    # llm.tokenize expects UTF-8 encoded bytes
    sys_msg_tokens = llm.tokenize(system_message.encode("utf-8"))
    new_msg_tokens = llm.tokenize(prompt.encode("utf-8"))
    num_new_msg_tokens = len(new_msg_tokens)
    num_sys_token = len(sys_msg_tokens)
    num_sys_msg_token = num_sys_token + num_new_msg_tokens

    assert (
        num_sys_msg_token < MAX_TOKENS
    ), f"Input exceeds maximum token limit of {MAX_TOKENS}. Current count: {num_sys_msg_token}"

    return num_new_msg_tokens, num_sys_token, num_sys_msg_token


def trim_history_if_needed(
    db: Session, db_messages: List[Message], num_total_tokens: int, num_sys_token: int
) -> None:
    """Trim conversation history if it exceeds token limits.
    If the total number of tokens exceeds 80% of the maximum token limit,
    this function removes the oldest messages from the history until the
    total token count falls below the threshold.
    """
    max_tokens_limit = (MAX_TOKENS * 0.8) - num_sys_token
    if num_total_tokens > max_tokens_limit:
        logger.warning(
            f"Total tokens {num_total_tokens} exceed 80% of max limit {max_tokens_limit}. Trimming history."
        )
        # Calculate how many tokens we need to remove
        num_current = sum(msg.num_tokens for msg in db_messages)
        # Remove oldest messages until we reach the limit
        while (num_current > max_tokens_limit) and len(db_messages) > 0:
            oldest_msg = db_messages.pop(0)
            db.delete(oldest_msg)
            num_current -= oldest_msg.num_tokens
        db.commit()


def save_conversation(
    db: Session,
    session_id: str,
    prompt: str,
    response_text: str,
    num_new_msg_tokens: int,
    num_response_tokens: int,
) -> None:
    """Save user prompt and LLM response to the database."""
    db_session = (
        db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    )
    db.add(
        Message(
            session_id=session_id,
            role="user",
            content=prompt,
            num_tokens=num_new_msg_tokens,
        )
    )
    db.add(
        Message(
            session_id=session_id,
            role="assistant",
            content=response_text,
            num_tokens=num_response_tokens,
        )
    )
    # Update session's last activity
    db_session.last_activity = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
