from fastapi import FastAPI
from contextlib import asynccontextmanager
from .model import load_model
from .api import router  # assuming you defined routes in api.py
from .chat_history_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = load_model()
    print("✅ Model loaded at startup")

    # Initialize database
    app.state.db_session = init_db()
    print("✅ Database initialized")

    yield
    print("🔻 Shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(router) # adding all api routes to the app