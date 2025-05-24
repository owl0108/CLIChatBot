import json
import os
from pathlib import Path
import typer

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
CONFIG_FILE = CONFIG_DIR / "chatbot_config.json"
# Default system message if none is set
DEFAULT_SYSTEM_MESSAGE = """You are a helpful, respectful and honest assistant. \
    Always answer as helpfully as possible, while being safe, and using the same language written by the user as a multilingual assistant. \
    Your answers should be detailed and comprehensive, but should not exceed more than few paragraphs. \
    """

def load_config():
    """Load configuration from file or create with defaults if it doesn't exist."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            typer.echo("Warning: Config file corrupted. Using defaults.")
    
    # Default configuration
    config = {
        "system_message": DEFAULT_SYSTEM_MESSAGE
    }
    
    # Save the default config
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    
    return config
    
def update_config(updates: dict):
    """Update specific keys in the config without replacing the entire file."""
    config = load_config()
    config.update(updates)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    return config