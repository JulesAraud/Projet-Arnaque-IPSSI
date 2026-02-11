from __future__ import annotations

from pathlib import Path
from scam_simulator.prompts.loader import load_prompt


from scam_simulator.config import Config
from scam_simulator.llm.providers import make_chat


class DirectorAgent:
    """
    Directeur de scénario : ne parle pas à l'utilisateur, produit un objectif court.
    """

    def __init__(self) -> None:
        self.llm = make_chat(Config.MODEL_DIRECTOR or "gpt-4.1-mini", temperature=0.2)
        self.system = load_prompt("director_system.txt")

    def analyze(self, user_input: str) -> str:
        prompt = (
            f"{self.system}\n\n"
            "Analyse le message de l'arnaqueur et donne UN objectif court pour Jeanne.\n"
            "Format strict: une seule phrase (pas de markdown).\n\n"
            f"Message arnaqueur: {user_input}"
        )
        msg = self.llm.invoke(prompt)
        return (msg.content or "").strip() or "Rester confuse et demander de répéter."
