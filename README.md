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

## Requirements

- Python 3.8+
- llama-cpp-python
- FastAPI
- Typer
- SQLAlchemy
- Uvicorn

This codebase was developed with **M2 macbook air with 16GB of memery**, and has not yet been tested in other enviroments.

## Getting started

1. Clone this repository using:

    ```bash
    git clone https://github.com/owl0108/CLIChatBot.git
    ```

2. Create your own virtual environment with Python 3.12.10 and at the project root, run:

    ```bash
    pip install -r requirements.txt
    ```

3. Once the installation is complete, at the project root, run the following to start the backend server:

    ```bash
    uvicorn src.backend.main:app     
    ```

4. In another terminal window, start the client by:

    ```bash
    python -m src.client.main chat     
    ```

### Clearning chat history

On the CLI interface, typing `/clear` will delete the chat history.

### Customize system message

A system message defines the behavior and context of the conversation. If you want to use your own system message,

```bash
python -m src.client.main update
```

will start an interactive session to edit the system message. The message will be saved in `config/chatbot_config.json`.

## Project Structure

```bash
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
├── .gitignore                  # Git ignore file for excluding sensitive/generated files
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
```

## License

This project is licensed under the [MIT License](LICENSE).
