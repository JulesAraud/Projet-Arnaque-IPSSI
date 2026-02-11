from __future__ import annotations

from typing import Optional, List

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
    AIMessage,
    BaseMessage,
)
from langchain_openai import ChatOpenAI

from scam_simulator.config import Config
from scam_simulator.prompts.loader import load_prompt
from scam_simulator.tools.soundboard import dog_bark, doorbell, coughing_fit, tv_background


class VictimAgent:
    """
    Victime (Jeanne Dubois) avec tool calling :
    - Le modèle peut appeler dog_bark/doorbell/coughing_fit/tv_background
    - On exécute les tools, puis on renvoie leur résultat au modèle
    """

    def __init__(self) -> None:
        self.tools = [dog_bark, doorbell, coughing_fit, tv_background]
        self.tool_by_name = {t.name: t for t in self.tools}

        model = Config.MODEL_VICTIM or "gpt-4.1-mini"

        # bind_tools => autorise le modèle à déclencher des tool calls
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.6,
            api_key=Config.OPENAI_API_KEY,
        ).bind_tools(self.tools)

        # prompt système robuste (pas de chemin relatif)
        self.system_template = load_prompt("victim_system.txt")

        # petite mémoire locale (optionnel)
        self.history: List[BaseMessage] = []

    def respond(self, user_input: str, objective: str, constraint: Optional[str] = None) -> str:
        system_text = self.system_template.format(
            dynamic_context=objective,
            audience_event=constraint or "Aucun"
        )

        messages: List[BaseMessage] = [SystemMessage(content=system_text)]
        messages.extend(self.history)
        messages.append(HumanMessage(content=user_input))

        # 1) Appel du modèle (peut renvoyer tool_calls)
        ai_msg: AIMessage = self.llm.invoke(messages)

        tool_calls = getattr(ai_msg, "tool_calls", None) or []

        # 2) Si le modèle veut appeler des tools -> exécuter -> re-appeler le modèle
        if tool_calls:
            tool_messages: List[ToolMessage] = []

            for call in tool_calls:
                name = call.get("name")
                args = call.get("args") or {}
                tool = self.tool_by_name.get(name)

                if tool is None:
                    output = f"[TOOL_ERROR: unknown_tool={name}]"
                else:
                    output = tool.invoke(args)

                tool_messages.append(
                    ToolMessage(
                        content=str(output),
                        tool_call_id=call.get("id", "")
                    )
                )

            # On ajoute la réponse outil au contexte et on redemande une réponse finale
            messages.append(ai_msg)
            messages.extend(tool_messages)

            final_msg: AIMessage = self.llm.invoke(messages)
            self._remember(user_input, final_msg.content)
            return final_msg.content

        # Réponse directe
        self._remember(user_input, ai_msg.content)
        return ai_msg.content

    def _remember(self, user_input: str, assistant_output: str) -> None:
        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=assistant_output))

        # limite mémoire
        if len(self.history) > 16:
            self.history = self.history[-16:]
