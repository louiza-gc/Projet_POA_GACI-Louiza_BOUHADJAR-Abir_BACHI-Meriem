from recipes import RECIPES

class Agent:
    def __init__(self, name="Cuisinier"):
        self.name = name
        self.score = 0

    def cook(self, recipe_name):
        if recipe_name not in RECIPES:
            print(f"[{self.name}] Désolé, je ne connais pas la recette '{recipe_name}' ")
            return

        recette = RECIPES[recipe_name]
        print(f"\nRecette demandée : {recipe_name}")
        print("Ingrédients nécessaires :", ", ".join(recette["ingredients"]))

        for action in recette["actions"]:
            print(f"[{self.name}] {action}")

        print(f"\n Plat {recipe_name} prêt !")
        self.score += 1
        print("Score actuel:", self.score)


if __name__ == "__main__":
    agent = Agent()

    while True:
        print("\n--- Menu ---")
        print("Recettes disponibles :", ", ".join(RECIPES.keys()))
        choix = input("Quelle recette veux-tu réaliser ? (ou 'quit' pour arrêter) : ").lower()

        if choix == "quit":
            print("Fin du jeu. Score final:", agent.score)
            break

        agent.cook(choix)
