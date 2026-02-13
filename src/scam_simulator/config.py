import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" ou "vertex"

    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_LOCATION = os.getenv("GCP_LOCATION", "europe-west1")
    VERTEX_MODEL = os.getenv("VERTEX_MODEL", "gemini-1.5-flash")

    MODEL_VICTIM = os.getenv("MODEL_VICTIM")
    MODEL_DIRECTOR = os.getenv("MODEL_DIRECTOR")
    MODEL_MODERATOR = os.getenv("MODEL_MODERATOR")
    
    MCP_SOUNDBOARD_COMMAND = os.getenv("MCP_SOUNDBOARD_COMMAND", "python")
    MCP_SOUNDBOARD_ARGS = os.getenv(
        "MCP_SOUNDBOARD_ARGS",
        "-m scam_simulator.tools.mcp_server"
    ).split()
