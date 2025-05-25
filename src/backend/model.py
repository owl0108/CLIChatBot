from llama_cpp import Llama

# TODO: separate model configuration from loading logic

MAX_TOKENS = 10000  # Maximum for unsloth/Llama-3.2-3B-Instruct-GGUF/Llama-3.2-3B-Instruct-IQ4_NL.gguf is around 13k


def load_model() -> Llama:
    print("Loading model...")
    llm = Llama.from_pretrained(
        repo_id="unsloth/Llama-3.2-3B-Instruct-GGUF",
        filename="Llama-3.2-3B-Instruct-IQ4_NL.gguf",
        verbose=False,
        chat_format="llama-3",
        n_ctx=MAX_TOKENS,  # goes up to 128k for llama-3.2
    )
    print("Model loaded.")
    return llm
