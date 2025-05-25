from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_DIR.mkdir(exist_ok=True)  # Ensure the database directory exists
DB_URL = f"sqlite:///{DATABASE_DIR / 'chat_history.db'}"  # Default database URL, can be overridden