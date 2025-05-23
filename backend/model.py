from llama_cpp import Llama

def load_model() -> Llama: 
    print("Loading model...")
    llm = Llama.from_pretrained(
        repo_id="unsloth/Llama-3.2-1B-Instruct-GGUF", filename="Llama-3.2-1B-Instruct-F16.gguf",
        verbose=False
    )
    print("Model loaded.")
    return llm