from importlib.resources import files

def load_prompt(filename: str) -> str:
    return (files("scam_simulator.prompts") / filename).read_text(encoding="utf-8")
