import json
import os
import requests

import typer

from .parameters import CONFIG_DIR, CONFIG_FILE, DEFAULT_SYSTEM_MESSAGE, API_URL


def load_config():
    """Load configuration from file or create with defaults if it doesn't exist."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            typer.echo("Warning: Config file corrupted. Using defaults.")

    # Default configuration
    config = {"system_message": DEFAULT_SYSTEM_MESSAGE}

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


def cleanup_session(session_id: str):
    # API_URL is a Path object, convert it to string for requests
    delete_url = f"{API_URL}/sessions/{session_id}"
    if session_id:
        try:
            response = requests.delete(delete_url)
            if response.status_code == 200:
                typer.echo(f"Session {session_id} cleaned up successfully.")
            else:
                typer.echo(
                    f"Failed to clean up session: {response.json().get('message', 'Unknown error')}"
                )
        except Exception as e:
            typer.echo(f"Error during cleanup: {e}")
    else:
        # Nothing to clean up
        pass
