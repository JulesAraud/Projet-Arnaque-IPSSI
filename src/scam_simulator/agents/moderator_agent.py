from __future__ import annotations

from pathlib import Path
from scam_simulator.prompts.loader import load_prompt

from typing import List

from scam_simulator.config import Config
from scam_simulator.llm.providers import make_chat


class ModeratorAgent:
    """
    Modérateur audience : reçoit une liste d'idées brutes, renvoie 3 choix propres et cohérents.
    """

    def __init__(self) -> None:
        self.llm = make_chat(Config.MODEL_MODERATOR or "gpt-4.1-mini", temperature=0.3)
        self.system = load_prompt("moderator_system.txt")

    def pick_three(self, proposals: List[str], context: str) -> List[str]:
        proposals_txt = "\n".join([f"- {p}" for p in proposals]) or "- (aucune proposition)"
        prompt = (
            f"{self.system}\n\n"
            "Contexte actuel:\n"
            f"{context}\n\n"
            "Propositions audience:\n"
            f"{proposals_txt}\n\n"
            "Tâche: garde uniquement les idées sûres et cohérentes, puis renvoie EXACTEMENT 3 choix.\n"
            "Format strict: 3 lignes, sans puces, sans numéros.\n"
        )
        msg = self.llm.invoke(prompt)
        lines = [l.strip() for l in (msg.content or "").splitlines() if l.strip()]
        # fallback si le modèle fait n'importe quoi
        while len(lines) < 3:
            lines.append("La télé est trop forte")
        return lines[:3]
