from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from scam_simulator.config import Config
from scam_simulator.agents.victim_agent import VictimAgent
from scam_simulator.agents.director_agent import DirectorAgent
from scam_simulator.agents.moderator_agent import ModeratorAgent
from scam_simulator.orchestration.state import SimulationState
from scam_simulator.orchestration.audience import collect_proposals, run_vote


console = Console()


def run_simulation() -> None:
    if not Config.OPENAI_API_KEY:
        console.print("[red]ERREUR: OPENAI_API_KEY manquant. Mets-le dans .env[/red]")
        return

    victim = VictimAgent()
    director = DirectorAgent()
    moderator = ModeratorAgent()
    state = SimulationState()

    console.print(Panel.fit("SIMULATEUR D'ARNAQUE (LLM + Tools)\nTape 'quit' pour quitter", title="Projet Arnaque"))

    while state.running:
        scammer = input("Arnaqueur > ").strip()
        if scammer.lower() == "quit":
            break

        # Directeur -> objectif dynamique
        state.current_objective = director.analyze(scammer)

        # Audience tous les 3 tours
        if state.turn % 3 == 0 and state.turn != 0:
            proposals = collect_proposals()
            if proposals:
                choices = moderator.pick_three(proposals, context=state.current_objective)
            else:
                # fallback si personne ne propose
                choices = ["Quelqu'un sonne à la porte", "Le chien aboie fort", "Quinte de toux"]
            state.audience_constraint = run_vote(choices)

 
        reply = victim.respond(
            user_input=scammer,
            objective=state.current_objective,
            constraint=state.audience_constraint,
        )

        console.print(Panel(reply, title="Jeanne", subtitle=f"objectif: {state.current_objective}"))
        state.turn += 1
