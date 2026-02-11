import random


class ModeratorAgent:

    def generate_choices(self):

        options = [
            "Quelqu'un sonne à la porte",
            "Le chien aboie",
            "La télé est trop forte",
            "Quinte de toux",
            "Le téléphone sonne"
        ]

        return random.sample(options, 3)
