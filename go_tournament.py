import os
import time

# Paramètres
display_mode = 2  # 0: Affichage normal, 1: Rapide, 2: Sans affichage (Turbo)
arenas = range(5) # De 0 à 4
positions = ["False", "True"] # Position départ normale puis inversée

print("Démarrage du tournoi...")

for arena in arenas:
    print(f"--- ARENA {arena} ---")
    for pos in positions:
        print(f"Position inversée: {pos}")
        # Construction de la commande
        # Rappel des arguments : config_file arena position display_mode
        cmd = f"py -3.12 tetracomposibot.py config_Paintwars {arena} {pos} {display_mode}"
        
        # Exécution
        os.system(cmd)
        
        # Petite pause pour respirer entre deux matchs (facultatif)
        time.sleep(1)

print("Tournoi terminé !")