import tkinter as tk
import time
import threading
import random

# --- Paramètres de la grille ---
TAILLE = 7  # 7x7
DELAI = 0.5  # secondes entre les déplacements

# --- Recettes ---
recettes = {
    "salade": ["tomate", "laitue", "oignon"],
    "sandwich": ["pain", "fromage", "jambon"]
}

# --- Ingrédients disponibles ---
ingredients_disponibles = ["tomate", "laitue", "oignon", "pain", "fromage", "jambon"]

# --- Grille initiale ---
# V = vide, C = comptoir, F = zone finale, A = agent
grille = [["V" for _ in range(TAILLE)] for _ in range(TAILLE)]
comptoir = (0, TAILLE-2)
zone_finale = (0, TAILLE-1)
agent_pos = [TAILLE-1, 0]  # départ en bas à gauche

grille[comptoir[0]][comptoir[1]] = "C"
grille[zone_finale[0]][zone_finale[1]] = "F"
grille[agent_pos[0]][agent_pos[1]] = "A"

# Placer des ingrédients aléatoirement
positions_ingredients = {}
for ingr in ingredients_disponibles:
    while True:
        x, y = random.randint(0, TAILLE-1), random.randint(0, TAILLE-1)
        if grille[x][y] == "V":
            grille[x][y] = ingr[0].upper()  # première lettre pour simplifier
            positions_ingredients[ingr] = (x, y)
            break

# --- Interface graphique ---
root = tk.Tk()
root.title("Mini Overcooked - Agent IA")

cell_labels = [[None for _ in range(TAILLE)] for _ in range(TAILLE)]
for i in range(TAILLE):
    for j in range(TAILLE):
        lbl = tk.Label(root, text=grille[i][j], font=("Helvetica", 16), width=4, height=2, borderwidth=1, relief="solid")
        lbl.grid(row=i, column=j)
        cell_labels[i][j] = lbl

# --- Fonctions ---
def update_grille():
    for i in range(TAILLE):
        for j in range(TAILLE):
            cell_labels[i][j].config(text=grille[i][j])
    root.update()

def move_agent(to_pos):
    global agent_pos
    # Déplacement simple : ligne puis colonne
    while agent_pos[0] != to_pos[0]:
        grille[agent_pos[0]][agent_pos[1]] = "V"
        agent_pos[0] += 1 if agent_pos[0] < to_pos[0] else -1
        grille[agent_pos[0]][agent_pos[1]] = "A"
        update_grille()
        time.sleep(DELAI)
    while agent_pos[1] != to_pos[1]:
        grille[agent_pos[0]][agent_pos[1]] = "V"
        agent_pos[1] += 1 if agent_pos[1] < to_pos[1] else -1
        grille[agent_pos[0]][agent_pos[1]] = "A"
        update_grille()
        time.sleep(DELAI)

def agent_preparer(recette_nom):
    recette = recettes[recette_nom]
    print(f"Agent prépare {recette_nom}")
    for ingr in recette:
        pos_ingr = positions_ingredients[ingr]
        move_agent(pos_ingr)
        print(f"Ramassé {ingr}")
        move_agent(comptoir)
        print(f"{ingr} déposé au comptoir")
    move_agent(zone_finale)
    print(f"{recette_nom} livré à la zone finale ✅")

def start_agent_thread():
    recette = entry.get().lower()
    if recette not in recettes:
        tk.messagebox.showerror("Erreur", f"Recette '{recette}' inconnue")
        return
    t = threading.Thread(target=agent_preparer, args=(recette,))
    t.start()

# --- Interface utilisateur ---
entry = tk.Entry(root, width=20, font=("Helvetica", 14))
entry.grid(row=TAILLE, column=0, columnspan=3, pady=10)
entry.insert(0, "salade")

btn_start = tk.Button(root, text="Démarrer l'agent", font=("Helvetica", 14), bg="#ff6347", fg="white", command=start_agent_thread)
btn_start.grid(row=TAILLE, column=3, columnspan=4, pady=10)

root.mainloop()
