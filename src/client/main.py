import requests
from typing import Optional

import typer

from .utils import load_config, update_config
from .utils import DEFAULT_SYSTEM_MESSAGE

app = typer.Typer()

API_URL = "http://localhost:8000/chat"


@app.command()
def chat():
    """Start an interactive chat with the LLaMA model running on the backend."""
    typer.echo("Type 'exit' or 'quit' to end the chat.")

    # Load the system message from config
    config = load_config()
    system_message = config["system_message"]

    while True:
        prompt = typer.prompt("You")

        if prompt.lower() in ["exit", "quit"]:
            typer.echo("Exiting chat.")
            break

        try:
            response = requests.post(
                API_URL, json={"prompt": prompt, "system_message": system_message}
            )
            response.raise_for_status()
            typer.echo(f"LLaMA: {response.json()['response']}")
        except requests.exceptions.RequestException as e:
            typer.echo(f"[Error] Failed to connect to backend: {e}")


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
        # Interactive mode: open editor or multi-line input
        current = config["system_message"]
        typer.echo(
            "Enter new system message (press Ctrl+D or Ctrl+Z on a new line to finish):"
        )
        typer.echo(f"Current: {current}")

        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            new_message = "\n".join(lines)
            if new_message.strip():  # empty string evaluates to False
                config["system_message"] = new_message
                update_config(config)
                typer.echo("System message updated successfully.")
            else:
                typer.echo("No changes made (empty input).")


if __name__ == "__main__":
    app()
