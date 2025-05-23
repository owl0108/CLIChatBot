# client/main.py
import typer
import requests

app = typer.Typer()

API_URL = "http://localhost:8000/chat"

@app.command()
def chat():
    """Start an interactive chat with the LLaMA model running on the backend."""
    typer.echo("Type 'exit' or 'quit' to end the chat.")
    
    while True:
        prompt = typer.prompt("You")
        
        if prompt.lower() in ["exit", "quit"]:
            typer.echo("Exiting chat.")
            break
        
        try:
            response = requests.post(API_URL, json={"prompt": prompt})
            response.raise_for_status()
            typer.echo(f"LLaMA: {response.json()['response']}")
        except requests.exceptions.RequestException as e:
            typer.echo(f"[Error] Failed to connect to backend: {e}")

if __name__ == "__main__":
    app()