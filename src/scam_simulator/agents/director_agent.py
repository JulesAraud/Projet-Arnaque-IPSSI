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
        self.llm = make_chat(Config.MODEL_DIRECTOR, temperature=0.2)
        self.system = load_prompt("director_system.txt")

    def analyze(self, user_input: str) -> str:
        t = user_input.lower()

        if any(k in t for k in ["2000", "euro", "€", "paiement", "virement", "iban", "rib", "carte", "cvc", "cvv"]):
            return "Refuser tout paiement, demander un courrier officiel, gagner du temps."
        if any(k in t for k in ["installer", "télécharger", "teamviewer", "anydesk", "contrôle à distance", "clic", "lien"]):
            return "Faire semblant d’être perdue sur l’ordinateur, ne rien installer, faire répéter."
        if any(k in t for k in ["microsoft", "support", "windows", "virus", "sécurité"]):
            return "Demander une preuve officielle, rester confuse, poser des questions simples."
        return "Rester polie, lente, confuse, et faire perdre du temps."
