import requests
from typing import Optional
import sys
import signal
from urllib.parse import urljoin

import typer

from .utils import load_config, update_config, cleanup_session
from .parameters import DEFAULT_SYSTEM_MESSAGE, API_URL

app = typer.Typer()
CHAT_URL = urljoin(API_URL, "chat/")


def signal_handler(sig, frame):
    """Handle termination signals by cleaning up the current session."""
    typer.echo("\nReceived termination signal. Closing session...")
    if active_session_id:
        cleanup_session(active_session_id)
    sys.exit(0)


@app.command()
def chat():
    """Start an interactive chat with the LLaMA model running on the backend."""
    global active_session_id
    active_session_id = None  # Initialize global variable to track session ID

    # Set up signal handlers for graceful termination
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

    typer.echo("Type 'exit' or 'quit' to end the chat.")
    typer.echo("Type '/clear' to clear conversation history.")

    # Load the system message from config
    config = load_config()
    system_message = config["system_message"]
    session_id = None
    try:
        while True:
            prompt = typer.prompt("You")

            # Handle exit command
            if prompt.lower() in ["exit", "quit"]:
                typer.echo("Exiting chat.")
                break

            # Handle chat history clearning
            elif prompt.lower() == "/clear":
                if session_id:
                    try:
                        response = requests.post(
                            CHAT_URL,
                            json={
                                "prompt": "< History clearance request >",
                                "system_message": system_message,
                                "session_id": session_id,
                                "clear_history": True,
                            },
                        )
                        response.raise_for_status()
                        typer.echo("Conversation history cleared.\n")
                    except requests.exceptions.RequestException as e:
                        typer.echo(f"[Error] Failed to clear history: {e}\n")
                else:
                    typer.echo("No active conversation to clear.\n")
            else:
                try:
                    response = requests.post(
                        CHAT_URL,
                        json={
                            "prompt": prompt,
                            "system_message": system_message,
                            "session_id": session_id,
                            "clear_history": False,
                        },
                    )
                    response.raise_for_status()
                    typer.echo(f"LLaMA: {response.json()['response']}\n")
                    session_id = response.json().get("session_id", session_id)
                    # Update the global variable when we get a session_id
                    active_session_id = session_id
                except requests.exceptions.RequestException as e:
                    typer.echo(f"[Error] Failed to connect to backend: {e}\n")
    finally:
        # Clean up operations on exit
        if active_session_id:
            cleanup_session(active_session_id)
            active_session_id = None  # Clear the global variable


@app.command()
def update(
    message: Optional[str] = typer.Option(
        None, "--message", "-m", help="New system message"
    ),
    view: bool = typer.Option(
        False, "--view", "-v", help="View current system message"
    ),
    reset: bool = typer.Option(
        False, "--reset", "-r", help="Reset to default system message"
    ),
):
    """Update, view, or reset the system message used for chat interactions."""
    config = load_config()

    if view:
        typer.echo("Current system message:")
        typer.echo(f"\n{config['system_message']}\n")
        return

    if reset:
        config["system_message"] = DEFAULT_SYSTEM_MESSAGE
        update_config(config)
        typer.echo("System message reset to default.")
        return

    if message:
        config["system_message"] = message
        update_config(config)
        typer.echo("System message updated successfully.")
    else:
        # Interactive mode: multi-line input with explicit end command
        current = config["system_message"]
        typer.echo(
            "Enter new system message (type ':save' on a new line to save, or ':cancel' to cancel):"
        )
        typer.echo(f"Current: {current}")

        lines = []
        typer.echo("\nNew system message (multi-line): ")
        while True:
            try:
                line = input()
                if line.strip() == ":save":
                    config["system_message"] = "\n".join(lines)
                    update_config(config)
                    typer.echo("System message updated successfully.")
                    break
                elif line.strip() == ":cancel":
                    typer.echo("Cancelled. No changes made.")
                    return
                lines.append(line)
            except KeyboardInterrupt:
                typer.echo("\nInput cancelled. No changes made.")
                return


if __name__ == "__main__":
    app()
