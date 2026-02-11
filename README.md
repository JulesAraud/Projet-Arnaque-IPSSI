# Projet Arnaque IPSSI — Simulateur Multi-Agents (LangChain + MCP)

## Membres du groupe
- ARAUD Jules

---

Commandes : 

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt

pip install -e .

copy .env.example .env

# Ensuite ouvrir .env et renseigné la clé API
"OPENAI_API_KEY=CLE_API"

Lancer : 

python -m scam_simulator.main

Ensuite (dans ta console pour le moment) :

tape les messages de l'arnaqueur

# Pour Quitter : quit

Notes MCP (important)

Le serveur MCP est utilisé en stdio et est démarré automatiquement via LangChain (client MCP).
Ne pas lancer manuellement :

python -m scam_simulator.tools.mcp_server



Structure du Projet Résumé : 

src/scam_simulator/
  agents/           # Victime / Directeur / Modérateur
  orchestration/    # Boucle simulation + audience
  tools/            # MCP server soundboard
  prompts/          # Prompts packagés (importlib.resources)
data/scripts/       # Scripts d’arnaque type (YAML)
