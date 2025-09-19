# Dictionnaire des recettes
# Chaque recette contient une liste d'ingrédients et des méthodes par ingrédient
recipes = {
    "salad": {
        "ingredients": ["salad", "tomato", "onion", "cucumber"],
        "methods": {
            "salad": ["rinse", "tear"],
            "tomato": ["rinse", "chop"],
            "onion": ["peel", "chop"],
            "cucumber": ["rinse", "slice"]
        }
    },
    "burger": {
        "ingredients": ["bread", "beef", "cheese", "tomato", "onion"],
        "methods": {
            "bread": ["toast"],
            "beef": ["grill"],
            "cheese": ["slice"],
            "tomato": ["rinse", "slice"],
            "onion": ["peel", "slice"]
        }
    }
}

def perform_method(ingredient, method):
    """Simule une action sur un ingrédient"""
    print(f"{method.capitalize()}ing {ingredient}...")