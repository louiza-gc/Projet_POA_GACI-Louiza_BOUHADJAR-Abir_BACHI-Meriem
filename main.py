import tkinter as tk
import time
from recipes import recipes  # Assure-toi que ton fichier recipes.py existe

available_ingredients = [
    "salad", "tomato", "onion", "carrot", "pepper",
    "chicken", "beef", "fish", "egg",
    "cheese", "bread", "cucumber"
]

# ------------------ Fenêtre pour indiquer que la commande est servie ------------------
def show_order_served():
    served_window = tk.Toplevel()
    served_window.title("Commande servie !")
    served_window.geometry("300x150")
    label = tk.Label(served_window, text="Commande servie !", font=("Arial", 24), fg="black")
    label.pack(expand=True)

# ------------------ Agent Chef ------------------
class ChefAgent:
    def __init__(self, canvas, chef_shape, output_widget):
        self.canvas = canvas
        self.chef = chef_shape
        self.output = output_widget
        self.x, self.y = self.canvas.coords(self.chef)[:2]

    def move_to(self, target_x, target_y, speed=5):
        while True:
            cx1, cy1, cx2, cy2 = self.canvas.coords(self.chef)
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
            self.canvas.move(self.chef, dx, dy)
            self.canvas.update()
            time.sleep(0.01)
        self.x, self.y = self.canvas.coords(self.chef)[:2]

    def pick_ingredient(self, ingredient_shape, ing_name):
        self.output.insert(tk.END, f"Picking {ing_name}...\n")
        self.output.yview_moveto(1)
        self.canvas.itemconfig(ingredient_shape, fill="green")
        self.canvas.update()
        time.sleep(0.5)

    def perform_method(self, ing_name, method):
        self.output.insert(tk.END, f"{method.capitalize()}ing {ing_name}...\n")
        self.output.yview_moveto(1)
        self.canvas.update()
        time.sleep(0.5)

    def serve(self, counter_shape):
        self.canvas.itemconfig(counter_shape, fill="red")
        self.output.insert(tk.END, "\nChef a servi le plat au comptoir !\n")
        self.output.yview_moveto(1)
        self.canvas.update()
        show_order_served()

# ------------------ Préparer le plat via l'agent ------------------
def prepare_dish(dish_order, chef_agent, ingredients_shapes, output_widget, prep_pos, counter_pos, counter_shape):
    output_widget.delete("1.0", tk.END)

    if dish_order not in recipes:
        output_widget.insert(tk.END, " Sorry, we don't know that recipe.\n")
        return

    recipe = recipes[dish_order]
    required_ingredients = recipe["ingredients"]
    methods = recipe["methods"]

    for ing in required_ingredients:
        if ing in available_ingredients:
            x1, y1, x2, y2 = canvas.coords(ingredients_shapes[ing])
            chef_agent.move_to(x1, y1)
            chef_agent.pick_ingredient(ingredients_shapes[ing], ing)

    # Plan de travail
    chef_agent.move_to(prep_pos[0], prep_pos[1])
    cours_text = canvas.create_text(
        (prep_pos[0]+prep_pos[0]+150)//2,
        prep_pos[1]+20,
        text="En cours...",
        font=("Arial", 12, "bold"),
        fill="black"
    )
    canvas.update()

    for ing in required_ingredients:
        if ing in methods:
            for action in methods[ing]:
                chef_agent.perform_method(ing, action)

    canvas.delete(cours_text)
    canvas.update()

    # Comptoir
    chef_agent.move_to(counter_pos[0], counter_pos[1])
    chef_agent.serve(counter_shape)

# ------------------ TKINTER GUI ------------------
root = tk.Tk()
root.title("Overcooked Switch game")
root.geometry("900x600")  # taille de départ

# Frame principale avec scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

main_canvas = tk.Canvas(main_frame)
main_canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=main_canvas.yview)
scrollbar.pack(side="right", fill="y")

main_canvas.configure(yscrollcommand=scrollbar.set)
main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))

# Frame interne pour tous les widgets
content_frame = tk.Frame(main_canvas)
main_canvas.create_window((0,0), window=content_frame, anchor="nw")

# --- Interface ---
title_label = tk.Label(content_frame, text="Overcooked Switch game", font=("Arial", 24, "bold"))
title_label.pack(pady=10)

entry = tk.Entry(content_frame, font=("Arial", 14))
entry.pack(pady=5)

# Zone de texte
output = tk.Text(content_frame, height=15, width=60, font=("Arial", 12))
output.pack(pady=10)

# Canvas pour chef et ingrédients
canvas = tk.Canvas(content_frame, width=850, height=400, bg="lightblue")
canvas.pack(pady=10)

# Chef
chef_shape = canvas.create_rectangle(20, 350, 60, 390, fill="red")
chef_agent = ChefAgent(canvas, chef_shape, output)

# Ingrédients
ingredients_shapes = {}
rows = 2
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
    ingredients_shapes[ing] = canvas.create_rectangle(x1, y1, x2, y2, fill="white")
    canvas.create_text((x1 + x2)//2, y1 - 10, text=ing, font=("Arial", 10, "bold"))

# Plan de travail
prep_x1 = 350
prep_y1 = 350
prep_x2 = 500
prep_y2 = 390
prep_area = canvas.create_rectangle(prep_x1, prep_y1, prep_x2, prep_y2, fill="grey")
canvas.create_text((prep_x1 + prep_x2)//2, prep_y1 - 10, text="Plan de travail", font=("Arial", 12, "bold"))

# Comptoir
counter_x1 = 750
counter_y1 = 50
counter_x2 = 800
counter_y2 = 150
counter = canvas.create_rectangle(counter_x1, counter_y1, counter_x2, counter_y2, fill="white")
canvas.create_text((counter_x1 + counter_x2)//2, counter_y1 - 10, text="Comptoir", font=("Arial", 12, "bold"))

# Bouton
button = tk.Button(
    content_frame,
    text="Prepare Dish",
    font=("Arial", 14),
    command=lambda: prepare_dish(
        entry.get().strip().lower(),
        chef_agent,
        ingredients_shapes,
        output,
        (prep_x1, prep_y1),
        (counter_x1, counter_y1),
        counter
    )
)
button.pack(pady=10)

root.mainloop()
