# CLIChatBot

CLIChatBot is a command-line interface chatbot application built on a server-client architecture. It features a lightweight CLI client for user interactions, and a [FastAPI](https://fastapi.tiangolo.com/) backend server that hosts the [Llama 3.2 language model](https://huggingface.co/unsloth/Llama-3.2-3B-Instruct-GGUF) for natural conversations. It also manages chat history using [SQLAlchemy](https://www.sqlalchemy.org/) for object-relational Mapping (ORM) and [SQLite](https://www.sqlite.org/) as a storage engine.

**Features**

- Interactive command-line chat interface
- Persistent chat history during the session (deleting when exiting)
- Configurable system messages to customize the assistant's behavior
- History management (clear conversation history during the session)

**Future Development Plan**

- Adding a functionality to recover past chat histories
- Code generation and execution (agentic AI)
- Multi-session handling (migrate from sqlite)

## Getting started

This codebase was developed with **M2 macbook air with 16GB of memery**, and has not yet been tested with othe enviroments.

Clone this repository using:

```bash
git clone https://github.com/owl0108/CLIChatBot.git
```

Create your own virtual environment with Python 3.12.10 and at the project root, run:

```bash
pip install -r requirements.txt
```

Once the installation is complete, at the project root, run:

```bash
uvicorn src.backend.main:app     
```

to start the backend server. On a separate terminal window, running:

```bash
python -m src.client.main chat     
```

will start the CLI interface in the terminal.

### Clearning chat history
On the CLI interface, typing `/clear` will delete the chat history.

### Use a custom system message

```bash
python -m src.client.main update
```


### 

### 




## Requirements

- Python 3.8+
- llama-cpp-python
- FastAPI
- Typer
- SQLAlchemy
- Uvicorn

## Project Structure

```
CLIChatBot/
├── config/                     # Configuration directory (created automatically)
│   └── chatbot_config.json     # Stores user preferences
├── database/                   # Database directory (created automatically)
│   └── chat_history.db         # SQLite database for chat history
├── src/
│   ├── backend/                # Backend server code
│   │   ├── __init__.py
│   │   ├── api.py              # FastAPI endpoints
│   │   ├── chat_history_db.py  # Database models and connection
│   │   ├── main.py             # FastAPI application entry point
│   │   ├── model.py            # LLM model loading and configuration
│   │   ├── parameters.py       # Backend configuration parameters
│   │   └── utils_api.py        # Utility functions for the API
│   └── client/                 # Client code
│       ├── __init__.py
│       ├── main.py             # CLI client entry point
│       ├── parameters.py       # Client configuration parameters
│       └── utils.py            # Client utility functions
└── run.sh                      # Script to start both backend and client
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CLIChatBot.git
   cd CLIChatBot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install llama-cpp-python fastapi uvicorn sqlalchemy typer requests
   ```

## Usage

### Starting the Application

Use the provided script to start both the backend server and client:

```
./run.sh
```

Alternatively, you can start them separately:

1. Start the backend server:
   ```
   cd CLIChatBot
   python -m uvicorn src.backend.main:app --reload
   ```

2. In another terminal, start the client:
   ```
   cd CLIChatBot
   python -m src.client.main chat
   ```

### Client Commands

- Chat with the AI:
  ```
  python -m src.client.main chat
  ```

- View the current system message:
  ```
  python -m src.client.main update --view
  ```

- Update the system message:
  ```
  python -m src.client.main update --message "Your new system message here"
  ```
  
- Reset the system message to default:
  ```
  python -m src.client.main update --reset
  ```

### Chat Commands

While in a chat session:
- Type `exit` or `quit` to end the session
- Type `/clear` to clear conversation history

## Creating a Startup Script

Create a `run.sh` script in your project root directory:

```bash
#!/bin/bash

# Navigate to project root directory
cd "$(dirname "$0")"

# Create necessary directories if they don't exist
mkdir -p config database

# Start the backend server
echo "🚀 Starting the backend server..."
python -m uvicorn src.backend.main:app --reload &
BACKEND_PID=$!

# Wait for the backend server to initialize
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend failed to start. Exiting."
    exit 1
fi

echo "✅ Backend server is running on http://localhost:8000"
echo "🤖 Starting CLI chat client..."

# Start the client
python -m src.client.main chat

# When client exits, stop the backend server
echo "👋 Shutting down backend server..."
kill $BACKEND_PID
wait $BACKEND_PID 2>/dev/null
echo "✅ Done!"
```

Make it executable:
```
chmod +x run.sh
```

## License

[Add your license information here]