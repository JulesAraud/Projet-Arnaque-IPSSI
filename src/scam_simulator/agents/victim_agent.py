class VictimAgent:

    def respond(self, user_input, objective, constraint=None):

        base = "Oh… je suis désolée… je ne comprends pas bien…"

        response = f"(Jeanne) {base} {objective}"

        if constraint:
            response += f" ({constraint})"

        return response
