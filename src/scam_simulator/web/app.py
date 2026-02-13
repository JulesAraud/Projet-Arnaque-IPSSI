from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

import streamlit as st

from scam_simulator.config import Config
from scam_simulator.agents.victim_agent import VictimAgent
from scam_simulator.agents.director_agent import DirectorAgent
from scam_simulator.agents.moderator_agent import ModeratorAgent


# -----------------------------
# Models (UI state)
# -----------------------------
@dataclass
class ChatTurn:
    role: str  # "scammer" | "jeanne" | "system"
    text: str
    meta: Optional[Dict[str, Any]] = None


# -----------------------------
# Helpers
# -----------------------------
def ensure_agents():
    if "victim" not in st.session_state:
        st.session_state.victim = VictimAgent()
    if "director" not in st.session_state:
        st.session_state.director = DirectorAgent()
    if "moderator" not in st.session_state:
        st.session_state.moderator = ModeratorAgent()


def init_state():
    st.session_state.turn = 0
    st.session_state.current_objective = "Répondre poliment mais lentement."
    st.session_state.audience_constraint = None

    st.session_state.chat: List[ChatTurn] = []
    st.session_state.logs: List[str] = []

    # Audience workflow
    st.session_state.audience_proposals: List[str] = []
    st.session_state.audience_choices: List[str] = []
    st.session_state.audience_vote: str = ""


def reset_all():
    # On conserve les agents pour éviter de relancer/recharger trop souvent.
    init_state()
    st.toast("Simulation réinitialisée ✅")


def add_log(msg: str):
    st.session_state.logs.append(f"{time.strftime('%H:%M:%S')} | {msg}")


def extract_sound_effects(text: str) -> List[str]:
    # Très simple : on détecte les tags retournés par tools
    effects = []
    for tag in [
        "[SOUND_EFFECT: DOG_BARKING]",
        "[SOUND_EFFECT: DOORBELL]",
        "[SOUND_EFFECT: COUGHING_FIT]",
        "[SOUND_EFFECT: TV_BACKGROUND_LOUD]",
    ]:
        if tag in text:
            effects.append(tag)
    return effects


def guardrails_check(text: str) -> Optional[str]:
    """
    Anti-catastrophe : si Jeanne lâche des infos sensibles, on bloque.
    (Basique, mais utile pour la note.)
    """
    lowered = text.lower()
    forbidden = ["iban", "rib", "numéro de carte", "carte bancaire", "cvc", "cvv", "mot de passe", "code sms"]
    if any(f in lowered for f in forbidden):
        return "🚫 La réponse contenait potentiellement des informations sensibles. Réponse bloquée."
    return None


# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(
    page_title="Simulateur d'Arnaque (MCP + LangChain)",
    layout="wide",
)

st.title("🎭 Simulateur d'Arnaque — Jeanne Dubois (LLM + MCP Tools)")

# Check config
if not Config.OPENAI_API_KEY:
    st.error("OPENAI_API_KEY manquant. Ajoute-le dans le fichier .env puis relance Streamlit.")
    st.stop()

ensure_agents()
if "chat" not in st.session_state:
    init_state()

with st.sidebar:
    st.header("⚙️ Contrôles")
    st.write("Tour :", st.session_state.turn)
    st.write("Objectif (Directeur) :")
    st.code(st.session_state.current_objective or "", language="text")
    st.write("Contrainte audience :")
    st.code(st.session_state.audience_constraint or "Aucune", language="text")

    st.divider()

    if st.button("🔄 Reset simulation", use_container_width=True):
        reset_all()

    st.divider()
    st.caption("MCP Soundboard")
    st.write("Command :", Config.MCP_SOUNDBOARD_COMMAND)
    st.write("Args :", " ".join(Config.MCP_SOUNDBOARD_ARGS))


col1, col2, col3 = st.columns([1.2, 2.2, 1.4], gap="large")

# -----------------------------
# Column 1: Scammer input
# -----------------------------
with col1:
    st.subheader("🕵️ Arnaqueur")
    scammer_text = st.text_area(
        "Message de l'arnaqueur",
        placeholder="Ex: Bonjour madame, je suis du support Microsoft...",
        height=160,
        key="scammer_input",
    )

    send = st.button("📨 Envoyer", type="primary", use_container_width=True)

    st.divider()
    st.caption("Astuce : tape 'quit' en CLI, ici utilise Reset.")

# -----------------------------
# Column 3: Audience
# -----------------------------
with col3:
    st.subheader("🗳️ Audience")

    # Add proposals
    proposal = st.text_input("Proposer un événement", placeholder="Ex: Quelqu'un sonne à la porte", key="proposal_input")
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("➕ Ajouter", use_container_width=True):
            p = (proposal or "").strip()
            if p:
                st.session_state.audience_proposals.append(p)
                st.session_state.proposal_input = ""
                add_log(f"[AUDIENCE] Proposition ajoutée: {p}")
            else:
                st.toast("Entre une proposition.", icon="⚠️")

    with c2:
        if st.button("🧹 Vider", use_container_width=True):
            st.session_state.audience_proposals = []
            st.session_state.audience_choices = []
            st.session_state.audience_vote = ""
            add_log("[AUDIENCE] Propositions vidées.")

    st.write("Propositions (max conseillé: 5) :")
    if st.session_state.audience_proposals:
        st.write("\n".join([f"- {p}" for p in st.session_state.audience_proposals]))
    else:
        st.info("Aucune proposition pour l'instant.")

    st.divider()

    if st.button("🤖 Modérateur: générer 3 choix", use_container_width=True):
        proposals = st.session_state.audience_proposals[:5]
        if not proposals:
            proposals = ["Quelqu'un sonne à la porte", "Le chien aboie fort", "Quinte de toux"]
        choices = st.session_state.moderator.pick_three(
            proposals=proposals,
            context=st.session_state.current_objective or "",
        )
        st.session_state.audience_choices = choices
        st.session_state.audience_vote = choices[0] if choices else ""
        add_log("[MODERATOR] 3 choix générés.")

    if st.session_state.audience_choices:
        st.write("Choisis l'événement :")
        st.session_state.audience_vote = st.radio(
            "Vote",
            st.session_state.audience_choices,
            index=0,
            label_visibility="collapsed",
        )
        if st.button("✅ Valider le vote", use_container_width=True):
            st.session_state.audience_constraint = st.session_state.audience_vote
            add_log(f"[AUDIENCE] Vote validé: {st.session_state.audience_constraint}")
            st.toast("Vote appliqué ✅")
    else:
        st.caption("Génère des choix pour voter.")

# -----------------------------
# Column 2: Conversation
# -----------------------------
with col2:
    st.subheader("💬 Conversation")
    st.caption("Historique + réponse de Jeanne + tools (si déclenchés)")

    # Display chat
    if not st.session_state.chat:
        st.info("Envoie un premier message de l'arnaqueur pour démarrer la simulation.")
    else:
        for t in st.session_state.chat[-20:]:
            if t.role == "scammer":
                st.markdown(f"**Arnaqueur :** {t.text}")
            elif t.role == "jeanne":
                st.markdown(f"**Jeanne :** {t.text}")
            else:
                st.caption(t.text)

    st.divider()
    st.subheader("🧾 Logs (debug)")
    if st.session_state.logs:
        st.code("\n".join(st.session_state.logs[-25:]), language="text")
    else:
        st.caption("Aucun log pour l'instant.")

# -----------------------------
# Actions: send scammer message
# -----------------------------
if send:
    scammer_text = (st.session_state.scammer_input or "").strip()
    if not scammer_text:
        st.toast("Écris un message d'arnaqueur.", icon="⚠️")
        st.stop()

    # Append scammer message
    st.session_state.chat.append(ChatTurn(role="scammer", text=scammer_text))

    # Director objective update
    add_log(f"[SCAMMER] {scammer_text}")
    obj = st.session_state.director.analyze(scammer_text)
    st.session_state.current_objective = obj
    add_log(f"[DIRECTOR] objectif -> {obj}")

    # Victim respond (MCP tools possible)
    reply = st.session_state.victim.respond(
        user_input=scammer_text,
        objective=st.session_state.current_objective,
        constraint=st.session_state.audience_constraint,
    )

    # Guardrails: prevent sensitive leakage
    blocked = guardrails_check(reply)
    if blocked:
        add_log("[GUARDRAIL] Réponse bloquée (info sensible détectée).")
        reply = blocked

    # Log sound effects if present
    effects = extract_sound_effects(reply)
    for e in effects:
        add_log(f"[TOOL_EFFECT] {e}")

    st.session_state.chat.append(ChatTurn(role="jeanne", text=reply))

    # Increment turn
    st.session_state.turn += 1

    # Clear input
    st.session_state.scammer_input = ""

    # Rerun to refresh UI
    st.rerun()
