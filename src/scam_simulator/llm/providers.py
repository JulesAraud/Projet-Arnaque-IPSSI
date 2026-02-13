from __future__ import annotations

from scam_simulator.config import Config


def make_chat(model: str | None = None, temperature: float = 0.2):
    provider = (Config.LLM_PROVIDER or "openai").lower()

    # 1) MOCK 
    if provider == "mock":
        from scam_simulator.llm.mock_chat import MockChatModel
        return MockChatModel(temperature=temperature, model=model or "mock")

    # 2) VERTEX
    if provider == "vertex":
        from langchain_google_vertexai import ChatVertexAI
        return ChatVertexAI(
            model=model or Config.VERTEX_MODEL,
            temperature=temperature,
            project=Config.GCP_PROJECT_ID,
            location=Config.GCP_LOCATION,
        )

    # 3) OPENAI
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=model or (Config.MODEL_VICTIM or "gpt-4.1-mini"),
        temperature=temperature,
        api_key=Config.OPENAI_API_KEY,
    )
