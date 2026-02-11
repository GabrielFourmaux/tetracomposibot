# Projet "robotique" IA&Jeux 2025
# TODO
# Binome:
#  Prénom Nom No_étudiant/e : _________
#  Prénom Nom No_étudiant/e : _________
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger"  # vous pouvez modifier le nom de votre équipe TODO
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory:int = 0  # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view, sensor_robot=None, sensor_team=None):

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # Robot 1 :
        if self.robot_id==0:
            if self.memory==0:
                translation = sensors[sensor_front]
                rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1
                sensor_to_robot.sort
                print(sensor_to_robot)
                #if sensor_to_robot[0] == 1:
                    #self.memory=1
                    #print("proche d'un robot")

                
        # Robot 2 :
        elif self.robot_id==1:
            if self.memory==0:
                translation = sensors[sensor_front]
                rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1
            
        # Robot 3 :
        elif self.robot_id==2:
            if self.memory==0:
                translation = sensors[sensor_front]
                rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1
            
        # Robot 4 :
        elif self.robot_id==3:
            if self.memory==0:
                translation = sensors[sensor_front]
                rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1
        
        return translation, rotation, False

