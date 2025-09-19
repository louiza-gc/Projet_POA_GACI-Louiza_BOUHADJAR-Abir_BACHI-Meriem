from recipes import RECIPES
<<<<<<< HEAD
=======

# Où trouver chaque ingrédient
TOOLS = {
    "tomates": "frigo",
    "oignon": "frigo",
    "concombre": "frigo",
    "laitue": "frigo",
    "pain": "placard",
    "fromage": "frigo",
    "jambon": "frigo",
    "spaghetti": "placard",
    "viande hachée": "frigo",
    "ail": "frigo",
}

# Décomposition des actions en étapes basiques
ACTIONS_DE_BASE = {
    "laver": ["prendre {ingrédient} du {lieu}", "aller à l’évier", "laver {ingrédient}"],
    "couper": ["prendre {ingrédient} du {lieu}", "prendre le couteau", "couper {ingrédient}"],
    "éplucher": ["prendre {ingrédient} du {lieu}", "prendre l’éplucheur", "éplucher {ingrédient}"],
    "émincer": ["prendre {ingrédient} du {lieu}", "prendre le couteau", "émincer {ingrédient}"],
    "cuire": ["prendre {ingrédient} du {lieu}", "allumer la plaque", "mettre {ingrédient} dans la casserole", "attendre cuisson"],
    "faire cuire": ["prendre {ingrédient} du {lieu}", "mettre {ingrédient} dans l’eau bouillante", "attendre cuisson"],
    "ajouter": ["prendre {ingrédient} du {lieu}", "ajouter {ingrédient} dans la préparation"],
    "mélanger": ["prendre la cuillère", "mélanger la préparation"],
    "assembler": ["prendre ingrédients préparés", "mettre ensemble sur l’assiette"],
    "fermer": ["prendre les tranches de pain", "fermer le sandwich"],
    "mettre": ["prendre {ingrédient} du {lieu}", "placer {ingrédient} sur le plat"],
}
>>>>>>> 400d2ac (Ajout des sous-actions dans game.py)

class Agent:
    def __init__(self, name="Cuisinier"):
        self.name = name
        self.score = 0

    def decompose_action(self, action, ingredient):
        """Décompose une action en sous-actions basiques"""
        for base, steps in ACTIONS_DE_BASE.items():
            if base in action:  
                lieu = TOOLS.get(ingredient, "plan de travail")
                for step in steps:
                    print(f"[{self.name}] {step.format(ingrédient=ingredient, lieu=lieu)}")
                return
        # sinon action générique
        print(f"[{self.name}] {action}")

    def cook(self, recipe_name):
        if recipe_name not in RECIPES:
            print(f"[{self.name}] Désolé, je ne connais pas la recette '{recipe_name}' ")
<<<<<<< HEAD
            return

        recette = RECIPES[recipe_name]
        print(f"\nRecette demandée : {recipe_name}")
        print("Ingrédients nécessaires :", ", ".join(recette["ingredients"]))

        for action in recette["actions"]:
            print(f"[{self.name}] {action}")
=======
            self.score -= 1
            return

        recette = RECIPES[recipe_name]
        print(f"\n[Client] J’ai commandé : {recipe_name}")
        print(f"[{self.name}] Très bien, je vais préparer ça !")

        for action in recette["actions"]:
            # Identifier l’ingrédient principal de l’action
            ingredient = None
            for ing in recette["ingredients"]:
                if ing in action:
                    ingredient = ing
                    break
            self.decompose_action(action, ingredient)
>>>>>>> 400d2ac (Ajout des sous-actions dans game.py)

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
