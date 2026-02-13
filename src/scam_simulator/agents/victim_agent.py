from __future__ import annotations

import asyncio
from typing import Optional, List

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
    AIMessage,
    BaseMessage,
)
from scam_simulator.llm.providers import make_chat

from langchain_mcp_adapters.client import MultiServerMCPClient

from scam_simulator.config import Config
from scam_simulator.prompts.loader import load_prompt


class VictimAgent:
    """
    Victime (Jeanne Dubois) :
    - Charge les tools via MCP (langchain-mcp-adapters) en stdio
    - Le client démarre automatiquement le serveur MCP en subprocess (command + args)
    """

    def __init__(self) -> None:
        self.system_template = load_prompt("victim_system.txt")

        self.llm = make_chat(
            model=Config.MODEL_VICTIM,
            temperature=0.6
        )


        self.history: List[BaseMessage] = []
        self._tools_loaded = False
        self._tools = []
        self._tool_by_name = {}

        # Client MCP (stdio) : le subprocess serveur sera lancé quand on récupère/appele les tools
        self._mcp_client = MultiServerMCPClient(
            {
                "soundboard": {
                    "transport": "stdio",
                    "command": Config.MCP_SOUNDBOARD_COMMAND,
                    "args": Config.MCP_SOUNDBOARD_ARGS,
                }
            }
        )

    async def _ensure_tools(self) -> None:
        if self._tools_loaded:
            return
        tools = await self._mcp_client.get_tools()  # récupère les tools MCP convertis en tools LangChain
        self._tools = tools
        self._tool_by_name = {t.name: t for t in tools}

        # On “bind” les tools au modèle (tool calling)
        self.llm = self.llm.bind_tools(self._tools)

        self._tools_loaded = True
    def _run_async(self, coro):
        """
        Exécute une coroutine même si un event loop tourne déjà (cas Streamlit).
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Streamlit / environnement avec loop déjà active
            import nest_asyncio  # type: ignore
            nest_asyncio.apply()
            return asyncio.get_event_loop().run_until_complete(coro)

        return asyncio.run(coro)

    def respond(self, user_input: str, objective: str, constraint: Optional[str] = None) -> str:
        # Load tools (1ère fois) — loop sync -> on encapsule async
        try:
            loop = asyncio.get_running_loop()
            # Si on est déjà dans une loop (rare ici), on planifie
            task = loop.create_task(self._ensure_tools())
            loop.run_until_complete(task)
        except RuntimeError:
            asyncio.run(self._ensure_tools())

        system_text = self.system_template.format(
            dynamic_context=objective,
            audience_event=constraint or "Aucun"
        )

        messages: List[BaseMessage] = [SystemMessage(content=system_text)]
        messages.extend(self.history)
        messages.append(HumanMessage(content=user_input))

        # 1) Appel du modèle (peut demander des tool calls MCP)
        ai_msg: AIMessage = self.llm.invoke(messages)
        tool_calls = getattr(ai_msg, "tool_calls", None) or []

        if tool_calls:
            tool_messages: List[ToolMessage] = []

            for call in tool_calls:
                name = call.get("name")
                args = call.get("args") or {}
                tool = self._tool_by_name.get(name)

                if tool is None:
                    output = f"[TOOL_ERROR: unknown_tool={name}]"
                else:
                    # tool MCP converti => invoke(args) déclenche une session MCP et appelle le serveur
                    output = tool.invoke(args)

                tool_messages.append(
                    ToolMessage(content=str(output), tool_call_id=call.get("id", ""))
                )

            messages.append(ai_msg)
            messages.extend(tool_messages)

            final_msg: AIMessage = self.llm.invoke(messages)
            self._remember(user_input, final_msg.content)
            return final_msg.content

        self._remember(user_input, ai_msg.content)
        return ai_msg.content

    def _remember(self, user_input: str, assistant_output: str) -> None:
        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=assistant_output))
        if len(self.history) > 16:
            self.history = self.history[-16:]
