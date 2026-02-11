from scam_simulator.config import Config


class LLMProvider:

    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY

    def is_configured(self):
        return self.api_key is not None
