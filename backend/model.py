from llama_cpp import Llama

def load_model() -> Llama: 
    print("Loading model...")
    llm = Llama.from_pretrained(
        repo_id="unsloth/Llama-3.2-3B-Instruct-GGUF",
        filename="Llama-3.2-3B-Instruct-IQ4_NL.gguf",
        verbose=False,
        chat_format="llama-3"
    )
    print("Model loaded.")
    return llm