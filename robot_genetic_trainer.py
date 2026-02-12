# robot_genetic_trainer.py - VERSION KAMIKAZE (EARLY STOPPING)
from robot import *
import math
import random

nb_robots = 0

class Robot_player(Robot):
    team_name = "KamikazeTrainer"
    robot_id = -1
    
    # Laisse vide pour chercher de nouveaux poids
    STARTING_WEIGHTS = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -0.12120627727507773, -0.1767044558613262, -0.18838026196536148, -0.013989301444108482, -0.15602130862143698, 0.15140473277167862, 0.1574931340403341, 0.37669115256557656, 1.0, 0.013217227844185997] 

    GENOME_SIZE = 18  
    EVALUATION_STEPS = 1500   # Durée totale d'un test réussi
    
    # --- PARAMÈTRES DE MORT SUBITE ---
    CHECKPOINT_STEPS = 150    # Vérification rapide au début
    MIN_SCORE_AT_CHECKPOINT = -5.0 # Si score inférieur à ça au checkpoint : ON TUE
    
    MUTATION_RATE = 0.15
    
    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name, team)
        
        # Initialisation
        self.parent_genome = self.create_random_genome()
        if len(self.STARTING_WEIGHTS) == self.GENOME_SIZE:
             self.parent_genome = self.STARTING_WEIGHTS[:]
             
        self.parent_score = -float('inf')
        self.current_genome = self.parent_genome[:] 
        self.current_score = 0
        self.step_counter = 0
        self.generation = 1
        self.attempts = 0 # Compteur d'essais (y compris les morts subites)

    def create_random_genome(self):
        # Biais positif vers l'avant pour éviter les robots qui reculent au spawn
        g = [random.uniform(-1, 1) for _ in range(self.GENOME_SIZE)]
        g[0] = random.uniform(0.5, 1.0) # Poids capteur avant -> Avancer
        g[16] = random.uniform(0.2, 1.0) # Biais translation -> Avancer
        return g

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # 1. Cerveau
        raw_trans = sum(sensors[i] * self.current_genome[i] for i in range(8)) + self.current_genome[16]
        raw_rot = sum(sensors[i] * self.current_genome[8+i] for i in range(8)) + self.current_genome[17]
        translation = math.tanh(raw_trans)
        rotation = math.tanh(raw_rot)

        # 2. Fitness (Maze Optimized)
        score = translation
        score -= abs(rotation) * 0.5 # Pénalité rotation
        
        # Pénalités Murales Sévères
        min_dist = min(sensors)
        if min_dist < 0.05: score -= 10.0 # Crash
        elif min_dist < 0.15: score -= 2.0 # Trop près
            
        # Bonus Centrage
        balance = 1.0 - abs(sensors[2] - sensors[6])
        score += balance * 0.1

        self.current_score += score
        self.step_counter += 1
        ask_reset = False

        # --- 3. MORT SUBITE (EARLY STOPPING) ---
        # Si on est au checkpoint et que le score est nul : on abandonne ce mutant.
        if self.step_counter == self.CHECKPOINT_STEPS:
            if self.current_score < self.MIN_SCORE_AT_CHECKPOINT:
                # KAMIKAZE : On ne perd pas de temps, on reset tout.
                # Si on n'a pas encore de bon parent, on génère un nouveau random complet
                if self.parent_score < 0:
                    self.current_genome = self.create_random_genome()
                    self.parent_genome = self.current_genome[:] # On oublie le parent pourri
                else:
                    # Sinon on refait une mutation du parent (autre essai)
                    self.current_genome = self.parent_genome[:]
                    idx = random.randint(0, self.GENOME_SIZE - 1)
                    self.current_genome[idx] += random.uniform(-0.5, 0.5)

                self.step_counter = 0
                self.current_score = 0
                self.attempts += 1
                return translation, rotation, True # RESET DU SIMULATEUR

        # --- 4. FIN NORMALE DE L'ÉVALUATION ---
        if self.step_counter >= self.EVALUATION_STEPS:
            self.attempts += 1
            if self.current_score > self.parent_score:
                self.parent_score = self.current_score
                self.parent_genome = self.current_genome[:]
                print(f"Gen {self.generation} (Essai {self.attempts}) | NEW BEST: {self.parent_score:.1f}")
                print(f"POIDS: {self.parent_genome}")
            
            # Préparation suivant
            self.current_genome = self.parent_genome[:]
            # Mutation
            nb_mutations = 2 if self.generation < 20 else 1
            for _ in range(nb_mutations):
                idx = random.randint(0, self.GENOME_SIZE - 1)
                self.current_genome[idx] += random.uniform(-self.MUTATION_RATE, self.MUTATION_RATE)
                self.current_genome[idx] = max(-1.0, min(1.0, self.current_genome[idx]))

            self.step_counter = 0
            self.current_score = 0
            self.generation += 1
            ask_reset = True 

        return translation, rotation, ask_reset