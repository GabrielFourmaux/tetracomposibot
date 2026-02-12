# config_Train.py
import arenas
import robot_genetic_trainer 

# --- PARAMÈTRES CRITIQUES ---
display_mode = 1
arena = 4

max_iterations = 10000000  

# --- AFFICHAGE ---
display_welcome_message = False
verbose_minimal_progress = True # Affiche les itérations pour voir que ça tourne
display_robot_stats = False
display_team_stats = False
display_tournament_results = False
display_time_stats = True

# --- INITIALISATION ---
def initialize_robots(arena_size=-1, particle_box=-1):
    x_center = 50
    y_center = 50
    
    robots = []
    # Robot entraîneur
    robots.append(robot_genetic_trainer.Robot_player(x_center, y_center, 0, name="Trainer", team="Lab"))
    return robots