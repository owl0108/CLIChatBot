from fastapi import Request, APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

@router.get("/")
def read_root():
    return {"message": "Chat API is running. Use POST /chat endpoint."}

@router.post("/chat")
def chat(req: ChatRequest, request: Request):
    """Handle chat requests by generating a response from the LLaMA model.
    Note that `request` is generated by FastAPI for internal representation for backend. (Not sent by the client)
    """
    llm = request.app.state.llm
    output = llm(req.prompt, max_tokens=128, stop=["\n"])
    return {"response": output["choices"][0]["text"].strip()}