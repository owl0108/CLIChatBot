from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_DIR.mkdir(exist_ok=True)  # Ensure the database directory exists
DB_URL = f"sqlite:///{DATABASE_DIR / 'chat_history.db'}"  # Default database URL, can be overridden

# Model parameters
# Maximum for unsloth/Llama-3.2-3B-Instruct-GGUF/Llama-3.2-3B-Instruct-IQ4_NL.gguf is around 13k
MAX_TOKENS = 10000
CHACHED_MODEL_PATH = Path("~/.cache/huggingface/hub/models--unsloth--Llama-3.2-3B-Instruct-GGUF/snapshots/571c76bbd17f77e948aeda72fabfe31b9597864a/Llama-3.2-3B-Instruct-IQ4_NL.gguf")