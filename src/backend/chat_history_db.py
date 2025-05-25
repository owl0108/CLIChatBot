import datetime
from pathlib import Path
from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"
DB_URL = f"sqlite:///{DATABASE_DIR / 'chat_history.db'}"  # Default database URL, can be overridden

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models. This is necessary to have shared metadata."""
    __abstract__ = True # Tells SQLAlchemy that this is an abstract base class and should not be mapped to a table.
    pass

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    
    session_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    last_activity = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey('chat_sessions.session_id'))
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    num_tokens = Column(Integer)  # Optional: store number of tokens used for the message
    
    session = relationship("ChatSession", back_populates="messages")

# Initialize database
def init_db(db_url=DB_URL):
    """Initialize the database and create tables. Creates a global SessionLocal."""
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    global SessionLocal
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal 

# # Helper functions
# def create_chat_session(session_id):
#     """Create a new chat session."""
#     db = SessionLocal()
#     chat_session = ChatSession(id=session_id)
#     db.add(chat_session)
#     db.commit()
#     db.close()

# def add_message(session_id, role, content):
#     """Add a message to a chat session."""
#     db = SessionLocal()
#     message = Message(session_id=session_id, role=role, content=content)
#     db.add(message)
    
#     # Update session's last activity
#     session = db.query(ChatSession).filter_by(id=session_id).first()
#     if session:
#         session.last_activity = datetime.datetime.now(datetime.timezone.utc)
    
#     db.commit()
#     db.close()

# def get_messages(session_id):
#     """Get all messages for a session."""
#     db = SessionLocal()
#     messages = db.query(Message).filter_by(session_id=session_id).order_by(Message.timestamp).all()
#     result = [{"role": msg.role, "content": msg.content} for msg in messages]
#     db.close()
#     return result

# def get_all_sessions():
#     """Get all chat sessions."""
#     db = SessionLocal()
#     sessions = db.query(ChatSession).all()
#     results = []
    
#     for session in sessions:
#         message_count = db.query(Message).filter_by(session_id=session.id).count()
#         results.append({
#             "session_id": session.id,
#             "created_at": session.created_at.isoformat(),
#             "last_activity": session.last_activity.isoformat(),
#             "message_count": message_count
#         })
    
#     db.close()
#     return results

# def delete_session(session_id):
#     """Delete a chat session and all its messages."""
#     db = SessionLocal()
#     session = db.query(ChatSession).filter_by(id=session_id).first()
#     if session:
#         db.delete(session)
#         db.commit()
#         db.close()
#         return True
#     db.close()
#     return False

def get_db():
    """Provide a database session and handle proper cleanup."""
    #TODO: verify that SessionLocal is already initialized
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()