from __future__ import annotations

from langchain_openai import ChatOpenAI
from scam_simulator.config import Config


def make_chat(model: str, temperature: float = 0.2) -> ChatOpenAI:
    """
    Fabrique un ChatOpenAI LangChain.
    La clé est lue via OPENAI_API_KEY (.env).
    """
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=Config.OPENAI_API_KEY,
    )
