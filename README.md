# Projet Arnaque IPSSI — Simulateur Multi-Agents (LangChain + MCP)

Ce projet est un simulateur interactif d’arnaque téléphonique basé sur une architecture multi-agents utilisant LangChain et le protocole MCP. 
Il met en scène une victime virtuelle nommée Jeanne Dubois, capable de résister à un arnaqueur grâce à une orchestration dynamique, un système de tools audio et une interface web.

Le système repose sur trois agents principaux : la victime, qui incarne une personne âgée confuse et résistante, le directeur de scénario, qui analyse les messages de l’arnaqueur et met à jour l’objectif stratégique, et le modérateur d’audience, qui filtre et sélectionne les propositions du public. 

Le projet vise à simuler des scénarios réalistes d’arnaque (support technique, bancaire, livraison), à démontrer une architecture multi-agents, à intégrer le tool calling via MCP, et à proposer un mode hors ligne permettant une démonstration sans dépendance externe.

Membre du groupe : ARAUD Jules.

# Installation : 

Cloner le dépôt GitHub, se placer dans le dossier du projet, créer un environnement virtuel avec `python -m venv venv`, activer l’environnement avec `.\venv\Scripts\Activate.ps1`,

Mettre à jour pip avec `pip install --upgrade pip`, installer les dépendances avec `pip install -r requirements.txt` puis `pip install -e .`, copier le fichier `.env.example` vers `.env` avec `copy .env.example .env`, puis modifier le fichier `.env` selon le mode choisi. 

Pour le mode recommandé hors ligne, définir `LLM_PROVIDER=mock`. Pour le mode OpenAI optionnel, définir `LLM_PROVIDER=openai` et `OPENAI_API_KEY=VOTRE_CLE_API`. 
Pour le mode Google Vertex optionnel, définir `LLM_PROVIDER=vertex`, `GCP_PROJECT_ID`, `GCP_LOCATION` et `VERTEX_MODEL`. Le fichier `.env` ne doit jamais être versionné.

# Lancement du projet :

En mode console avec `python -m scam_simulator.main`, en mode interface web avec `streamlit run src/scam_simulator/web/app.py`, puis ouverture dans un navigateur à l’adresse `http://localhost:8501`. 

L’utilisateur incarne l’arnaqueur et interagit avec Jeanne en saisissant ses messages. En mode console, la commande `quit` permet de quitter l’application.

Le projet utilise un serveur MCP pour la gestion des bruitages audio. Ce serveur fonctionne en stdio et est lancé automatiquement via LangChain par le client MCP. Il ne doit pas être lancé manuellement. 

Les providers LLM supportés sont le mode mock (par défaut, gratuit, hors ligne), OpenAI (optionnel, payant) et Vertex AI (optionnel, payant). Le mode mock garantit une démonstration fonctionnelle sans dépendance externe.

# Structure du projet : 

Le dossier `src/scam_simulator` contient les modules `agents` (victime, directeur, modérateur), `orchestration` (boucle principale et audience), `llm` (providers OpenAI, Vertex, Mock), `tools` (serveur MCP soundboard), `prompts` (prompts packagés), et `web` (interface Streamlit). 

Le dossier `data` contient les scripts de scénarios en YAML et les logs. Les tests peuvent être lancés avec `pytest`.

# Notes importantes : 

Aucune clé API n’est versionnée, le projet est compatible hors ligne, les prompts sont chargés via 
importlib.resources, et l’architecture est extensible. 

# Perspectives d’évolution : 

Intégration d’un LLM réel par défaut, interface web multi-utilisateurs, export d’historique, déploiement cloud, et analyse automatique des stratégies d’arnaque. Projet académique réalisé dans le cadre du Master 2 IA à l’IPSSI, usage pédagogique uniquement.
