from langchain_groq import ChatGroq
from .config import GROQ_API_KEY

# Ordered by most likely to be free on your key
MODELS_TO_TRY = [
    "openai/gpt-oss-20b",  # FREE - works today Oct 2026
    "llama-3.1-8b-instant", # may be enterprise for you
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]

def get_llm(temperature=0):
    last_error = None
    for model in MODELS_TO_TRY:
        try:
            print(f"Trying Groq model: {model}")
            llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=model, temperature=temperature)
            # quick test invoke to see if key has access
            # llm.invoke("hi")  # uncomment if you want to test immediately
            print(f"Using Groq model: {model}")
            return llm
        except Exception as e:
            print(f"Model {model} failed: {e}")
            last_error = e
            continue
    
    raise Exception(f"All Groq models failed. Last error: {last_error}. Check console.groq.com/docs/models")