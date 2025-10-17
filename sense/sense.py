'''
Sensor interface
'''
import random 

class Sensor:
    '''
    Class that implement the sensor interface
    Sensor Class: Create a class for the sensors. This class should include:

    Attributes for different types of sensors (e.g., type, range).
    Methods to gather data from the environment.
    '''

    def __init__(self, name : str, stype : str):
        self._name = name
        self._type = stype
        self._range = [0.0, 0.0]  #tuple min, tuple max --> polar coordinates more than 1 limit -- à voir
        self._value = None       # type image or tab or single value

    def __repr__(self):
        return f"I am {self._name}, a {self._type} reading {self._value}"
    
    def get_name(self): 
        return self._name
    
    def get_type(self): 
        return self._type
    
    def get_value(self): 
        return self._value
    
    def get_range(self): 
        return self._range
    
    def set_value(self, value : float):
        if value >= self._range[0] and value <= self._range[1]: 
            self._value=value
        return self._value
    
    def set_range(self, values : list):
        if len(values)==2:
            self._range[0] = min(values)
            self._range[1] = max(values)
        return self._range
    
    def collect_data(self, robot=None, environment=None):
        """
        Simule la lecture d'une valeur selon le type de capteur.
        (dans une simulation : aléatoire, ou dépend de la position du robot)
        """
        if self._type == "lidar":
            # Simule la détection d'obstacles : distance libre (0 à 10)
            value = random.uniform(0.0, 10.0)

        elif self._type == "video":
            # Simule une "image" -> ici juste un identifiant d'objet visible
            possible_objects = ["nothing", "tree", "rock", "charger"]
            value = random.choice(possible_objects)

        elif self._type == "depth_sensor":
            # Simule la profondeur moyenne d'une scène
            value = random.uniform(0.25, 5.0)

        elif self._type == "bumper":
            # Détection de collision
            value = random.choice([True, False])

        elif self._type == "battery":
            # Lire la batterie du robot
            value = robot.get_battery() if robot else 100.0

        else:
            print(f"[WARNING] Capteur {self._type} inconnu")
            value = None

        self._value = value
        return self._value
    
class Sense:
    """ Use of the sensors """
    def __init__(self, robot, environment):
        self.robot = robot
        self.environment = environment

        # Ensemble de capteurs bruts
        self.sensors = {
            "lidar_left": Sensor("L0", "lidar"),
            "lidar_front": Sensor("L1", "lidar"),
            "lidar_right": Sensor("L2", "lidar"),
            "bumper": Sensor("B1", "bumper"),
            "battery": Sensor("BAT", "battery")
        }

    def perceive(self):
        perception = {}
        for name, sensor in self.sensors.items():
            perception[name] = sensor.collect_data(robot=self.robot, environment=self.environment)

        x, y = self.robot._pos["x"], self.robot._pos["y"]
        width, height = self.environment["map_size"]

        # Positions relatives des lidars
        front = left = right = (x, y)
        if self.robot._orientation == 0:  # droite
            front = (x+1, y)
            left  = (x, y-1)
            right = (x, y+1)
        elif self.robot._orientation == 180:  # gauche
            front = (x-1, y)
            left  = (x, y+1)
            right = (x, y-1)
        elif self.robot._orientation == 90:  # haut
            front = (x, y-1)
            left  = (x-1, y)
            right = (x+1, y)
        elif self.robot._orientation == 270:  # bas
            front = (x, y+1)
            left  = (x+1, y)
            right = (x-1, y)

        lidars = {}
        obstacles = self.environment.get("obstacles", set())  # ensemble des cases obstacles
        lidars["front"] = 0.0 if front in obstacles or front[0] > 9 or front[0] < 0 or front[1] > 9 or front[1] < 0 else 1.0
        lidars["left"]  = 0.0 if left  in obstacles or left[0] > 9 or left[0] < 0 or left[1] > 9 or left[1] < 0 else 1.0
        lidars["right"] = 0.0 if right in obstacles or right[0] > 9 or right[0] < 0 or right[1] > 9 or right[1] < 0 else 1.0

        next_x, next_y = front
        obstacle_ahead = (
            lidars["front"] == 0.0 or
            perception.get("bumper", False)
        )

        perception_simple = {
            "battery": perception.get("battery", 100),
            "position": (x, y),
            "obstacle_ahead": obstacle_ahead,
            "lidar_front": lidars["front"],
            "lidar_left": lidars["left"],
            "lidar_right": lidars["right"]
        }
        #print(f"Lidars : {lidars["left"]}, {lidars["front"]}, {lidars["right"]}")
        return perception_simple



if __name__ == "__main__":
    s1=Sensor("L1", "lidar")
    print(s1)
    s1.collect_data()
