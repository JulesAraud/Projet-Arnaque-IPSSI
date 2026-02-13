from __future__ import annotations

import random
import re
from typing import Any, Dict, List, Optional, Sequence, Union

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)


class MockChatModel:
    """
    Faux LLM (gratuit) compatible avec le minimum attendu par ton code :
    - .invoke(messages|str) -> AIMessage
    - .bind_tools(tools) -> self

    Il simule :
    - un tool calling (en renvoyant tool_calls)
    - une réponse finale après ToolMessage
    """

    def __init__(self, temperature: float = 0.3, model: str = "mock") -> None:
        self.temperature = temperature
        self.model = model
        self._tools = []
        self._tool_names = set()

    def bind_tools(self, tools: List[Any]) -> "MockChatModel":
        self._tools = tools or []
        self._tool_names = {getattr(t, "name", "") for t in self._tools}
        return self

    def invoke(self, input_: Union[str, Sequence[BaseMessage]], **kwargs: Any) -> AIMessage:
        # Accept both str and list[BaseMessage] (LangChain style)
        if isinstance(input_, str):
            return AIMessage(content=self._simple_text(input_))

        messages = list(input_)
        last_human = next((m for m in reversed(messages) if isinstance(m, HumanMessage)), None)
        last_tool = next((m for m in reversed(messages) if isinstance(m, ToolMessage)), None)
        system = next((m for m in messages if isinstance(m, SystemMessage)), None)

        human_text = (last_human.content if last_human else "") or ""
        system_text = (system.content if system else "") or ""

        # Si on vient de recevoir un tool output => produire une réponse finale “Jeanne”
        if last_tool is not None:
            return AIMessage(content=self._after_tool(system_text, human_text, str(last_tool.content)))

        # Sinon : décider s'il faut faire un tool call (simulé)
        tool_call = self._maybe_tool_call(system_text, human_text)
        if tool_call:
            return AIMessage(content="", tool_calls=[tool_call])

        # Réponse simple
        return AIMessage(content=self._jeanne_reply(system_text, human_text))

    # ------------------------
    # Heuristics
    # ------------------------
    def _simple_text(self, prompt: str) -> str:
        # Utilisé si on appelle invoke("...") en string.
        # On renvoie une phrase neutre plutôt que "Bonjour (mode mock)".
        return "D’accord… (mode mock)"


    def _parse_objective(self, system_text: str) -> str:
        m = re.search(r"Current Context:\s*(.*)", system_text)
        return (m.group(1).strip() if m else "").strip()

    def _parse_audience(self, system_text: str) -> str:
        m = re.search(r"Audience Event:\s*(.*)", system_text)
        return (m.group(1).strip() if m else "").strip()

    def _maybe_tool_call(self, system_text: str, human_text: str) -> Optional[Dict[str, Any]]:
        """
        Renvoie un tool_call dict si on veut déclencher un tool.
        Format attendu par ton VictimAgent : {"id": "...", "name": "...", "args": {...}}
        """
        if not self._tool_names:
            return None

        t = human_text.lower()
        audience = self._parse_audience(system_text).lower()

        # Priorité à l'audience
        if "sonne" in audience or "porte" in audience:
            if "doorbell" in self._tool_names:
                return {"id": "mock-1", "name": "doorbell", "args": {}}

        # Si l'arnaqueur devient pressant -> chien ou toux
        if any(k in t for k in ["vite", "urgent", "tout de suite", "immédiatement", "dépêchez"]):
            if "dog_bark" in self._tool_names and random.random() < 0.6:
                return {"id": "mock-2", "name": "dog_bark", "args": {}}
            if "coughing_fit" in self._tool_names:
                return {"id": "mock-3", "name": "coughing_fit", "args": {}}

        # Tech support -> télé
        if any(k in t for k in ["microsoft", "windows", "virus", "support"]):
            if "tv_background" in self._tool_names and random.random() < 0.35:
                return {"id": "mock-4", "name": "tv_background", "args": {}}

        return None

    def _after_tool(self, system_text: str, human_text: str, tool_output: str) -> str:
        obj = self._parse_objective(system_text) or "Gagner du temps."
        if "DOORBELL" in tool_output:
            return f"{tool_output}\nOh… on sonne à la porte… je reviens… ne raccrochez pas hein…  \n_(Objectif: {obj})_"
        if "DOG_BARKING" in tool_output:
            return f"{tool_output}\nOh là là… Poupoune devient folle… excusez-moi…  \n_(Objectif: {obj})_"
        if "COUGHING_FIT" in tool_output:
            return f"{tool_output}\n*khm khm*… pardon… je tousse… j’ai la gorge sèche…  \n_(Objectif: {obj})_"
        if "TV_BACKGROUND" in tool_output:
            return f"{tool_output}\nOh… la télé était trop forte… je baisse…  \n_(Objectif: {obj})_"
        return f"{tool_output}\nEuh… oui… alors…  \n_(Objectif: {obj})_"

    def _jeanne_reply(self, system_text: str, human_text: str) -> str:
        obj = self._parse_objective(system_text) or "Répondre poliment mais lentement."
        audience = self._parse_audience(system_text)

        t = human_text.lower()

        # Intent (petit moteur de règles)
        if any(k in t for k in ["2000", "euro", "€", "paiement", "virement", "iban", "rib", "carte", "cvc", "cvv"]):
            base = "Oh non non… je ne fais jamais de paiement au téléphone… c’est mon fils qui s’occupe de ça."
            follow = "Vous pouvez m’envoyer un courrier officiel si c’est sérieux."
        elif any(k in t for k in ["installer", "télécharger", "teamviewer", "anydesk", "contrôle à distance", "clic", "lien"]):
            base = "Attendez… je vois bien l’ordinateur, mais je ne sais pas où il faut cliquer…"
            follow = "Je ne télécharge rien sans mon petit-fils, vous comprenez."
        elif any(k in t for k in ["microsoft", "support", "windows", "virus", "sécurité", "ordinateur"]):
            base = "Ah bon… un virus ? C’est grave ça… mais je ne comprends pas, je n’ai rien fait."
            follow = "Vous avez un numéro officiel, monsieur ?"
        else:
            base = "Oh… je suis désolée… je ne comprends pas très bien…"
            follow = "Vous pouvez répéter doucement ?"

        # Audience event (si présent)
        aud = ""
        if audience and audience.lower() != "aucun":
            aud = f" (Je suis distraite: {audience})"

        # Ajoute l’objectif du directeur (ça fait “orchestration” même en mock)
        return f"{base} {follow}{aud}  \n_(Objectif: {obj})_"
