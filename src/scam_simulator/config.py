import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Provider: mock | openai | vertex | hf
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").strip().lower()

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Google Vertex / Gemini (service account)
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_LOCATION = os.getenv("GCP_LOCATION", "europe-west1")
    VERTEX_MODEL = os.getenv("VERTEX_MODEL", "gemini-1.5-flash")

    # Hugging Face
    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

    # Models (per agent) – defaults OK
    MODEL_VICTIM = os.getenv("MODEL_VICTIM", "gpt-4.1-mini")
    MODEL_DIRECTOR = os.getenv("MODEL_DIRECTOR", "gpt-4.1-mini")
    MODEL_MODERATOR = os.getenv("MODEL_MODERATOR", "gpt-4.1-mini")

    # MCP soundboard server (stdio)
    MCP_SOUNDBOARD_COMMAND = os.getenv("MCP_SOUNDBOARD_COMMAND", "python")

    # Ex: "-m scam_simulator.tools.mcp_server"
    _mcp_args_raw = os.getenv("MCP_SOUNDBOARD_ARGS", "-m scam_simulator.tools.mcp_server").strip()
    MCP_SOUNDBOARD_ARGS = _mcp_args_raw.split() if _mcp_args_raw else []
    
    # gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # ollama
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

