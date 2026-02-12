from robot import * 
import math
import numpy as np

nb_robots = 0
debug = False

def mutation(param):
    new=param
    mut=[(random.random()-0.5)/10 for i in range(len(param))]
    for i in range(len(param)):
        new[i]+=mut[i]
    return new,mut

def fitness(coords):
    s=0
    for x,y in coords:
        for a,b in coords:
            s+=(x-a)**2+(y-b)**2
    return s

class Robot_player(Robot):

    team_name = "Optimizer"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    it_per_evaluation = 1000
    trial = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]
    x_1=0
    y_1=0
    coords=set()
    best_overall_score=0
    stuck=0
    last_mutation=[0 for i in range(9)]
    last_successfull=False

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.y_1 = x_0
        self.x_1 = y_0
        self.theta_0 = theta_0
        self.param = [-0.006884943410049266, 2.0369751801255296, 0.6393038364208256, 1.0100742856263958, 0.8277362156223403, 1.3552293320528044, -0.5497005744877436, -1.1081729988535922, -1.7497844884652958]
        self.it_per_evaluation = it_per_evaluation
        self.current_score=0
        self.bestScore=0
        self.best_params=self.param
        self.best_trial=0
        
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        x=round(self.x/2)
        y=round(self.y/2)
        if (x,y) not in self.coords:
            self.current_score+=1
            self.coords.add((x,y))

        if self.iteration % self.it_per_evaluation == 0:
        	
            if self.iteration > 0:
                self.xs=[0]
                ys=[0]
                """print ("\tparameters           =",self.param)
                print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                print ("\tdistance from origin =",math.sqrt((self.x-self.x0)**2+(self.y-self.y0)**2))
                """
                """if self.trial>=500:
                    self.it_per_evaluation=1000
                    self.param=self.best_params"""
    
                self.coords=set()

                if self.trial%9==0:
                    self.stuck+=1
                    #if self.trial%300==3:
                        #print(self.current_score)
                    if self.current_score>self.bestScore:
                        print(self.last_successfull)
                        self.last_successfull=True
                        print(self.stuck,self.bestScore)
                        self.stuck=0
                        #print(self.bestScore,self.best_params)
                        self.bestScore=self.current_score
                        self.best_params=self.param
                        self.best_trial=self.trial/9
                        if self.bestScore>self.best_overall_score:
                            print(self.bestScore,self.best_params)
                            self.best_overall_score=self.bestScore
                    else:
                        self.last_successfull=False
                    self.current_score=0
                    if self.stuck==100:
                        print("stuck")
                        self.stuck=0
                        #print(self.best_params, self.bestScore,self.best_trial)
                        self.param=[-0.006884943410049266, 2.0369751801255296, 0.6393038364208256, 1.0100742856263958, 0.8277362156223403, 1.3552293320528044, -0.5497005744877436, -1.1081729988535922, -1.7497844884652958]
                        #map 2: [-0.12492588566460801, 1.5339590816608244, 0.8412221474936135, 0.6532907577132708, -0.11688505615266442, 1.4041710753292742, -0.3851689646258929, -0.5502788849081325, -0.6900753807282004]
                        
                        self.best_params=self.param
                        self.bestScore=0
                        self.best_trial=self.trial
                    else:
                        if self.last_successfull:
                            self.param=[self.param[i]+self.last_mutation[i] for i in range(len(self.param))]
                        else:
                            self.param,self.last_mutation = mutation(self.best_params)
                self.trial=self.trial+1
                #print ("Trying strategy no.",self.trial)
                self.iteration = self.iteration + 1
                rotations=[0,120,240]
                xs=[49,4,94]
                self.theta0=rotations[self.trial%3]
                self.x0=xs[self.trial%3]
                return 0, 0, True # ask for reset

    
        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( 0 + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4]*sensors[sensor_left] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_right] + self.param[7] * sensors[sensor_front_right] + self.param[8]* (random.random()-0.5) )


        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        self.iteration = self.iteration + 1    
        self.x_1=self.x


        return translation, rotation, False
