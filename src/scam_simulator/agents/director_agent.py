class DirectorAgent:

    def analyze(self, user_input: str) -> str:

        text = user_input.lower()

        if "installer" in text or "télécharger" in text:
            return "Faire semblant de ne pas trouver le bouton."

        if "payer" in text or "carte" in text:
            return "Refuser poliment et détourner la discussion."

        return "Rester confuse et demander de répéter."
