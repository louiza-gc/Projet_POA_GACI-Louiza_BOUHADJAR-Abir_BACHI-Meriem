import tkinter as tk
from tkinter import messagebox

# --- Dictionnaire de recettes avec étapes ---
recettes = {
    "salade": [
        {"ingredient": "tomate", "action": "couper"},
        {"ingredient": "laitue", "action": "mettre dans le bol"},
        {"ingredient": "oignon", "action": "couper"},
        {"ingredient": "laitue", "action": "mélanger"}
    ],
    "sandwich": [
        {"ingredient": "pain", "action": "mettre sur la planche"},
        {"ingredient": "fromage", "action": "mettre sur le pain"},
        {"ingredient": "jambon", "action": "mettre sur le fromage"},
        {"ingredient": "pain", "action": "fermer le sandwich"}
    ],
    "soupe": [
        {"ingredient": "eau", "action": "verser dans la casserole"},
        {"ingredient": "carotte", "action": "couper"},
        {"ingredient": "pomme de terre", "action": "couper"},
        {"ingredient": "carotte", "action": "mettre dans la casserole"},
        {"ingredient": "pomme de terre", "action": "mettre dans la casserole"},
        {"ingredient": "mélanger", "action": "mélanger la soupe"}
    ],
    "pizza margherita": [
        {"ingredient": "pâte", "action": "étaler"},
        {"ingredient": "sauce tomate", "action": "mettre sur la pâte"},
        {"ingredient": "mozzarella", "action": "mettre sur la sauce"},
        {"ingredient": "cuire", "action": "mettre au four"}
    ],
}

# --- Variables globales ---
panier = []   # État actuel du panier
score = 0     # Score global

# --- Fonctions de l'agent ---
def agent_preparer(commande):
    """Agent cuisinier qui suit les étapes exactes pour préparer la recette."""
    global score
    if commande not in recettes:
        messagebox.showwarning("Erreur", "Cette recette n’existe pas.")
        score -= 5
        update_score()
        return

    recette = recettes[commande]

    # L’agent suit chaque étape
    for etape in recette:
        ingredient = etape["ingredient"]
        action = etape["action"]
        # Affiche l'action dans la console et ajoute l'ingrédient
        print(f"L’agent {action} : {ingredient}")
        ajouter_ingredient(ingredient)

    # Vérification : succès si tous les ingrédients requis sont dans le panier
    ingredients_requis = [e["ingredient"] for e in recette]
    if sorted(panier) == sorted(ingredients_requis):
        messagebox.showinfo("Bravo !", f"L’agent a préparé une {commande} ✅")
        score += 10
    else:
        messagebox.showerror("Raté !", f"L’agent a raté la {commande} 😅")
        score -= 5

    update_score()
    reset_panier()

def ajouter_ingredient(ingredient):
    """Ajoute un ingrédient au panier et met à jour l'affichage."""
    panier.append(ingredient)
    update_panier()
    root.update()  # Rafraîchir l'interface

def reset_panier():
    """Vide le panier et réinitialise le champ de saisie."""
    global panier
    panier = []
    update_panier()
    entry.delete(0, tk.END)

def update_panier():
    """Met à jour l'affichage du panier."""
    panier_label.config(text="Panier : " + ", ".join(panier) if panier else "Panier vide")

def update_score():
    """Met à jour l'affichage du score."""
    score_label.config(text=f"Score : {score}")

# --- Interface graphique ---
root = tk.Tk()
root.title("Mini Overcooked avec Agent et Étapes")

# Label pour le score
score_label = tk.Label(root, text=f"Score : {score}", font=("Arial", 14, "bold"))
score_label.pack(pady=5)

# Champ de saisie pour la commande
entry = tk.Entry(root, width=20)
entry.pack(pady=5)
entry.insert(0, "salade")  # Exemple par défaut

# Bouton pour envoyer la commande à l'agent
btn_valider = tk.Button(root, text="Envoyer la commande à l’agent",
                        command=lambda: agent_preparer(entry.get().lower()))
btn_valider.pack(pady=10)

# Label pour afficher le contenu du panier
panier_label = tk.Label(root, text="Panier vide")
panier_label.pack(pady=5)

root.mainloop()
