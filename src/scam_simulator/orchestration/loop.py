from scam_simulator.agents.victim_agent import VictimAgent
from scam_simulator.agents.director_agent import DirectorAgent
from scam_simulator.agents.moderator_agent import ModeratorAgent
from scam_simulator.orchestration.state import SimulationState
from scam_simulator.orchestration.audience import run_vote


def run_simulation():

    victim = VictimAgent()
    director = DirectorAgent()
    moderator = ModeratorAgent()

    state = SimulationState()

    print("\n=== SIMULATEUR D'ARNAQUE ===")
    print("Tape 'quit' pour quitter\n")

    while state.running:

        user_input = input("Arnaqueur > ")

        if user_input.lower() == "quit":
            break

        # Analyse directeur
        state.current_objective = director.analyze(user_input)

        # Audience tous les 3 tours
        if state.turn % 3 == 0 and state.turn != 0:

            choices = moderator.generate_choices()
            state.audience_constraint = run_vote(choices)

        # Réponse victime
        response = victim.respond(
            user_input,
            state.current_objective,
            state.audience_constraint
        )

        print("\nJeanne >", response, "\n")

        state.turn += 1
