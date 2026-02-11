def run_vote(choices):

    print("\n--- Vote audience ---")

    for i, c in enumerate(choices, start=1):
        print(f"{i}. {c}")

    winner = choices[0]

    print("Choix retenu :", winner)

    return winner
