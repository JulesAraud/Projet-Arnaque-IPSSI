from __future__ import annotations

import sys
from mcp.server.fastmcp import FastMCP

# Serveur MCP (transport stdio)
mcp = FastMCP("arnaque-soundboard")


@mcp.tool()
def dog_bark() -> str:
    """Aboiement de chien (Poupoune s'énerve). Utile pour interrompre un interlocuteur pressant."""
    return "[SOUND_EFFECT: DOG_BARKING]"


@mcp.tool()
def doorbell() -> str:
    """Sonnette (livraison/visite). Utile pour faire patienter l'arnaqueur."""
    return "[SOUND_EFFECT: DOORBELL]"


@mcp.tool()
def coughing_fit() -> str:
    """Quinte de toux ~10 secondes."""
    return "[SOUND_EFFECT: COUGHING_FIT]"


@mcp.tool()
def tv_background() -> str:
    """Télé en fond très forte (ex: Les Feux de l'Amour)."""
    return "[SOUND_EFFECT: TV_BACKGROUND_LOUD]"


def main() -> None:
    # NE PAS print sur stdout (stdio transport) -> si besoin, logguez sur stderr
    print("MCP soundboard server starting (stdio)...", file=sys.stderr)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
