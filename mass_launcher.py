import subprocess
import time
import sys

NB_INSTANCES = 6 

print(f"Lancement de {NB_INSTANCES} entraînements en parallèle...")

processes = []

for i in range(NB_INSTANCES):
    cmd = f'start "Trainer_{i+1}" cmd /k py -3.12 tetracomposibot.py config_Train'
    subprocess.Popen(cmd, shell=True)
    time.sleep(1) 

print("Tout est lancé ! Surveille les fenêtres.")
print("Dès qu'une fenêtre affiche un bon score (> 300 ou 400), copie les POIDS.")