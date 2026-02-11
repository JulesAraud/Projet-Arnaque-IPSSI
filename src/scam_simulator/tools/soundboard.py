from langchain_core.tools import tool

@tool
def dog_bark() -> str:
    """Joue un aboiement de chien."""
    return "[SOUND_EFFECT: DOG_BARKING]"

@tool
def doorbell() -> str:
    """Joue une sonnette."""
    return "[SOUND_EFFECT: DOORBELL]"

@tool
def coughing_fit() -> str:
    """Simule une quinte de toux."""
    return "[SOUND_EFFECT: COUGHING_FIT]"

@tool
def tv_background() -> str:
    """Bruit de télé en fond."""
    return "[SOUND_EFFECT: TV_BACKGROUND_LOUD]"
