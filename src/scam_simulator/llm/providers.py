from __future__ import annotations

from scam_simulator.config import Config
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_google_genai import ChatGoogleGenerativeAI



def _fallback_mock(model: str | None, temperature: float):
    from scam_simulator.llm.mock_chat import MockChatModel
    return MockChatModel(temperature=temperature, model=model or "mock")


def make_chat(model: str | None = None, temperature: float = 0.2):
    provider = (Config.LLM_PROVIDER or "mock").strip().lower()

    # 1) MOCK (gratuit / offline)
    if provider == "mock":
        return _fallback_mock(model, temperature)

    # 2) HUGGING FACE (Inference Providers / Endpoint)
    if provider == "hf":
        try:
            if not Config.HUGGINGFACEHUB_API_TOKEN:
                return _fallback_mock(model, temperature)

            from langchain_huggingface import HuggingFaceEndpoint
            return HuggingFaceEndpoint(
                repo_id=Config.HF_MODEL,
                huggingfacehub_api_token=Config.HUGGINGFACEHUB_API_TOKEN,
                temperature=temperature,
                max_new_tokens=256,
                provider="hf-inference",
            )

        except Exception as e:
            print("HF ERROR:", repr(e))
            return _fallback_mock(model, temperature)



    # 3) VERTEX (service account)
    if provider == "vertex":
        from langchain_google_vertexai import ChatVertexAI
        return ChatVertexAI(
            model=model or Config.VERTEX_MODEL,
            temperature=temperature,
            project=Config.GCP_PROJECT_ID,
            location=Config.GCP_LOCATION,
        )
        
    # 4) gemini
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=Config.GEMINI_MODEL,
            google_api_key=Config.GEMINI_API_KEY,
            temperature=temperature,
        )

    #5 ) ollama
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=Config.OLLAMA_MODEL,
            base_url=Config.OLLAMA_BASE_URL,
            temperature=temperature,
        )


    # 6) OPENAI
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=model or (Config.MODEL_VICTIM or "gpt-4.1-mini"),
        temperature=temperature,
        api_key=Config.OPENAI_API_KEY,
    )
