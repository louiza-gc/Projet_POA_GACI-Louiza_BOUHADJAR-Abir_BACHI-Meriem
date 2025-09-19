import tkinter as tk
import time
from recipes import recipes  # Assure-toi que ton fichier recipes.py existe

# Liste d'ingrédients disponibles
available_ingredients = [
    "salad", "tomato", "onion", "cucumber", "carrot", "pepper",
    "chicken", "beef", "fish", "egg",
    "cheese", "bread"
]

# ------------------ Fenêtre pour le score ------------------
def show_score(stars):
    score_window = tk.Toplevel()
    score_window.title("Score !")
    score_window.geometry("300x200")
    score_label = tk.Label(
        score_window,
        text='⭐' * stars,
        font=("Arial", 48),
        fg="gold"
    )
    score_label.pack(expand=True)

# ------------------ Déplacement et action du chef ------------------
def move_chef_to(canvas, chef, target_x, target_y, speed=5):
    while True:
        cx1, cy1, cx2, cy2 = canvas.coords(chef)
        dx = dy = 0
        if cx1 < target_x:
            dx = min(speed, target_x - cx1)
        elif cx1 > target_x:
            dx = -min(speed, cx1 - target_x)
        if cy1 < target_y:
            dy = min(speed, target_y - cy1)
        elif cy1 > target_y:
            dy = -min(speed, cy1 - target_y)
        if dx == 0 and dy == 0:
            break
        canvas.move(chef, dx, dy)
        canvas.update()
        time.sleep(0.01)

def perform_action(canvas, ingredient_shape):
    canvas.itemconfig(ingredient_shape, fill="green")
    canvas.update()
    time.sleep(0.5)

# ------------------ Préparer le plat ------------------
def prepare_dish(dish_order, canvas, chef, ingredients_shapes, output_widget):
    output_widget.delete("1.0", tk.END)

    if dish_order not in recipes:
        output_widget.insert(tk.END, " Sorry, we don't know that recipe.\n")
        return

    recipe = recipes[dish_order]
    required_ingredients = recipe["ingredients"]
    methods = recipe["methods"]

    prepared_ingredients = []

    for ing in required_ingredients:
        if ing in available_ingredients:
            output_widget.insert(tk.END, f"Going to pick {ing}...\n")
            output_widget.update()
            # Déplacer le chef vers l'ingrédient
            x1, y1, x2, y2 = canvas.coords(ingredients_shapes[ing])
            move_chef_to(canvas, chef, x1, y1)
            output_widget.insert(tk.END, f"Preparing {ing}...\n")
            output_widget.update()
            perform_action(canvas, ingredients_shapes[ing])
            prepared_ingredients.append(ing)

    # Calcul du score
    total = len(required_ingredients)
    prepared = len(prepared_ingredients)
    if total == 0:
        stars = 0
    else:
        ratio = prepared / total
        if ratio == 1:
            stars = 3
        elif ratio >= 0.5:
            stars = 2
        else:
            stars = 1

    if sorted(prepared_ingredients) == sorted(required_ingredients):
        output_widget.insert(tk.END, f"\n {dish_order} ready to serve! ({', '.join(prepared_ingredients)})\n")
    else:
        output_widget.insert(tk.END, "\n Missing ingredients! Could not prepare the dish.\n")

    # Afficher le score
    show_score(stars)

# ------------------ TKINTER GUI ------------------
root = tk.Tk()
root.title("Overcooked Switch game")
root.geometry("900x900")

# Label de titre centré
title_label = tk.Label(root, text="Overcooked Switch game", font=("Arial", 24, "bold"))
title_label.pack(pady=10)

# Champ de saisie
entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=5)

# Zone de texte pour afficher la préparation
output = tk.Text(root, height=10, width=60, font=("Arial", 12))
output.pack(pady=10)

# Canvas pour chef et ingrédients
canvas = tk.Canvas(root, width=750, height=300, bg="lightblue")
canvas.pack(pady=10)

# Chef = carré rouge
chef = canvas.create_rectangle(20, 250, 60, 290, fill="red")

# Placer tous les ingrédients en grille
ingredients_shapes = {}
rows = 2  # 2 lignes
cols = (len(available_ingredients) + 1) // 2
spacing_x = 100
spacing_y = 100
start_x = 50
start_y = 50

for i, ing in enumerate(available_ingredients):
    row = i // cols
    col = i % cols
    x1 = start_x + col * spacing_x
    y1 = start_y + row * spacing_y
    x2 = x1 + 40
    y2 = y1 + 40
    ingredients_shapes[ing] = canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")
    # Ajouter le nom au-dessus
    canvas.create_text((x1 + x2)//2, y1 - 10, text=ing, font=("Arial", 10, "bold"))

# Bouton "Prepare Dish"
button = tk.Button(
    root,
    text="Prepare Dish",
    font=("Arial", 14),
    command=lambda: prepare_dish(entry.get().strip().lower(), canvas, chef, ingredients_shapes, output)
)
button.pack(pady=10)

root.mainloop()
