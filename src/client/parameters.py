from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"
CONFIG_FILE = CONFIG_DIR / "chatbot_config.json"
API_URL = "http://localhost:8000"

# Default system message if none is set
DEFAULT_SYSTEM_MESSAGE = """You are a helpful, respectful and honest assistant. \
    Always answer as helpfully as possible, while being safe, and using the same language written by the user as a multilingual assistant. \
    Your answers should be detailed, comprehensive but concise. \
    """


