from llama_cpp import Llama
from .parameters import MAX_TOKENS, CHACHED_MODEL_PATH

# TODO: separate model configuration from loading logic
def load_model() -> Llama:
    print("Loading model...")
    # check if the model is already cached
    # from_pretrained will raise error without an internet connection
    # even when not downloading the model
    model_path = CHACHED_MODEL_PATH.expanduser().resolve()
    if model_path.exists():
        llm = Llama(
            model_path=str(model_path),
            verbose=False,
            chat_format="llama-3",
            n_ctx=MAX_TOKENS,
        )
    else:
        llm = Llama.from_pretrained(
            repo_id="unsloth/Llama-3.2-3B-Instruct-GGUF",
            filename="Llama-3.2-3B-Instruct-IQ4_NL.gguf",
            verbose=False,
            chat_format="llama-3",
            n_ctx=MAX_TOKENS,  # goes up to 128k for llama-3.2
        )
    print("Model loaded.")
    return llm
