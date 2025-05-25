import datetime
from pathlib import Path
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from .parameters import DB_URL  # Import the default DB_URL from parameters
SessionLocal = None  # Global variable to hold the session factory


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models. This is necessary to have shared metadata."""
    __abstract__ = True  # Tells SQLAlchemy that this is an abstract base class and should not be mapped to a table.
    pass


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    session_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    last_activity = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )
    messages = relationship(
        "Message", back_populates="session", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey("chat_sessions.session_id"))
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    num_tokens = Column(
        Integer
    )  # Optional: store number of tokens used for the message

    session = relationship("ChatSession", back_populates="messages")


# Initialize database
def init_db(db_url=DB_URL):
    """Initialize the database and create tables. This is called inside the FastAPI lifespan."""
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    global SessionLocal
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal


def get_db():
    """Provide a database session and handle proper cleanup."""
    assert (
        SessionLocal is not None
    ), "Database session factory is not initialized. Call init_db() first."
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
