# Projet "robotique" IA&Jeux 2025
# TEAM CHALLENGER - STRATEGIE "BLITZKRIEG"
# Binome:
#  Prénom Nom No_étudiant/e : _________
#  Prénom Nom No_étudiant/e : _________

from robot import *
import math
import random

nb_robots = 0

class Robot_player(Robot):

    team_name = "Blitzkrieg"
    robot_id = -1
    # La mémoire est utilisée comme un automate à états pour la manœuvre d'évasion
    # memory = 0: Etat normal (exploration)
    # memory > 0: Etat d'évasion (recule puis pivote)
    memory: int = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view, sensor_robot=None, sensor_team=None):
        translation = 1.0
        rotation = 0.0

        # --- AUTOMATE A ETATS GERÉ PAR self.memory ---

        # ETAT 1 : MANOEUVRE D'EVASION EN COURS
        if self.memory > 0:
            self.memory += 1
            # Phase 1: Reculer (pendant 15 itérations)
            if self.memory < 15:
                translation = -1.0
                rotation = 0.0
            # Phase 2: Pivoter brusquement (pendant 20 itérations de plus)
            elif self.memory < 35:
                translation = 0.0
                # Le sens de rotation dépend si le robot est pair ou impair pour varier
                rotation = 1.0 if self.robot_id % 2 == 0 else -1.0
            # Fin de la manœuvre, retour à l'état normal
            else:
                self.memory = 0
            
            return translation, rotation, False # On sort directement, la manœuvre est prioritaire

        # ETAT 0 : EXPLORATION RAPIDE (COMPORTEMENT PAR DEFAUT)
        # Détection de blocage : si on est trop proche d'un mur, on déclenche l'état 1
        if sensors[0] < 0.45 and self.memory == 0:
            self.memory = 1 # Déclenche la manœuvre au prochain 'step'
            translation = -1.0 # Commence déjà à reculer
            return translation, rotation, False

        # Comportement Braitenberg Agressif
        # Poids optimisés pour l'évitement rapide
        translation = 1.0 # Toujours à fond !
        rotation = (sensors[1] * 1.5 + sensors[2] * 0.5) - (sensors[7] * 1.5 + sensors[6] * 0.5)
        
        # Ajout d'une touche de chaos pour l'individualité
        # Plus l'ID est grand, plus le robot est "imprévisible"
        rotation += (random.random() - 0.5) * 0.2 * (self.robot_id + 1)

        # REFLEXE AGRESSIF : "BELIER"
        # Prioritaire sur le Braitenberg : si un ennemi est collé devant, on charge !
        if sensor_view[0] == 2 and sensors[0] < 0.2 and sensor_team[0] != self.team_name:
            translation = 1.0
            rotation = 0.0 # Droit sur lui
        
        # Sécurité pour rester dans les bornes
        translation = max(-1.0, min(1.0, translation))
        rotation = max(-1.0, min(1.0, rotation))

        return translation, rotation, False