from __future__ import annotations
from typing import List


def collect_proposals() -> List[str]:
    print("\nAudience > Propose 1 à 5 idées (ligne vide pour finir).")
    proposals: List[str] = []
    while True:
        line = input("Audience idée > ").strip()
        if not line:
            break
        proposals.append(line)
        if len(proposals) >= 5:
            break
    return proposals


def run_vote(choices: List[str]) -> str:
    print("\n--- Vote audience ---")
    for i, c in enumerate(choices, start=1):
        print(f"{i}. {c}")

    raw = input("Choisis 1/2/3 (entrée = 1 par défaut) > ").strip()
    if raw in {"1", "2", "3"}:
        winner = choices[int(raw) - 1]
    else:
        winner = choices[0]

    print("Gagnant :", winner)
    print("---------------------\n")
    return winner
