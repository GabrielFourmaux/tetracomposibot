# Nicolas
# 2025-03-24
#
# comportement par défaut
# 
def get_bit(memory, bit_index):
    return (memory >> bit_index) & 1

def set_bit(memory, bit_index):
    return memory | (1 << bit_index)

def clear_bit(memory, bit_index):
    return memory & ~(1 << bit_index)

def get_value(memory, start, size):
    value=0
    for i in range(size):
        value+=get_bit(memory,i+start)*2**i

    return value

def set_value(memory,start,size,new_value):
    for i in range(size):
        if new_value & 1==0:
            memory=clear_bit(memory, start+i)
        else:
            memory=set_bit(memory,start+i)
        new_value=new_value>>1
    
    return memory

a=32768
print(bin(a))
print(bin(get_value(a,2,3)))
print(bin(set_value(a,3,2,2)),bin(2))

def navigation(sensors,memory,sens,peux_tourner):
    veux_tourner=False
    if sens==-1:
        front=sensor_rear
        right=sensor_left
        left=sensor_right
    else:
        front=sensor_front
        right=sensor_right
        left=sensor_left

    if memory!=0:
        return 0,memory,sens,False
    
    dé=random.randint(1,3)
    
    if sensors[right]==1 and sensors[left]==1:
        if peux_tourner and dé==1:
            return 0,random.choice([-1,1]), sens,False
        else:
            veux_tourner=1
    if sensors[right]==1:
        if peux_tourner and dé==1:
            return 0,-1, sens,False
        else:
            veux_tourner=1
    if sensors[left]==1:
        if peux_tourner and dé==1:
            return 0,1, sens,False
        else:
            veux_tourner=1
    

    if sensors[front]<0.15:
        if sensors[right]==sensors[left]==1:
            return 0,random.choice([-1,1]),sens,False
        if sensors[right]==1:
            print("droite")
            return 0,(-1),sens,False
        elif sensors[left]==1:
            print("gauche")
            return 0,1,sens,False
        else:
            print("back")
            return -sens,0,-sens,False
    
    print("tout droit")
    return sens,0,sens,veux_tourner


from robot import * 

nb_robots = 0
debug = False 

class Robot_player(Robot):
    
    team_name = "Professor X"
    robot_id = -1
    iteration = 0
    avg=0
    signe=0
    memory=0
    peux_tourner=5
    veux_tourner=False
    sens=1
    cooldown=0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        translation = sensors[sensor_front]*0.5+0.2
        rotation = 0.2 * sensors[sensor_left] + 0.2 * sensors[sensor_front_left] - 0.2 * sensors[sensor_right] - 0.2 * sensors[sensor_front_right] + (random.random()-0.5)*1. #+ sensors[sensor_front] * 0.1
        if debug == True:
            if self.iteration % 100 == 0 and self.robot_id == 0:
                print ("Robot",self.robot_id,"(team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)
        avg=0
        for d in sensors:
            avg+=d/8
        self.avg=(self.avg*self.iteration+avg)/(self.iteration+1)
        print(self.avg)
        self.iteration = self.iteration + 1

        if not self.veux_tourner or self.peux_tourner==0:
            self.peux_tourner=2

        if self.veux_tourner and self.cooldown==0:
            self.peux_tourner-=1

        if self.cooldown>0:
            self.cooldown-=1

        translation,rotation,self.sens,self.veux_tourner=navigation(sensors,self.signe,self.sens,(self.peux_tourner==0))
        print(sensors,self.signe,self.sens)
        print("angle:"+str(self.theta))
        if rotation==-1:
            self.signe=-1
            self.memory+=1
        elif rotation==1:
            self.signe=1
            self.memory+=1
        else:
            self.memory=0
            self.signe=0
            
        if self.memory>=9:
            self.cooldown=7
            self.memory=0
            self.signe=0
        
        """print(translation, rotation, self.memory)
        print("angle:"+str(self.theta))
        print(sensors)
        print(self.sens)"""
        #print(sensors,self.signe,self.sens)

        return translation, rotation, False