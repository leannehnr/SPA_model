'''
Physical robot interface
'''
from ..sense import sense as s

class Robot:
    '''
    Class that implement the physical robot interface

    This will be the main class that represents the robot. It should contain:

    Attributes for the robot's body (e.g., size, weight, battery level).
    Methods to initialize the robot and manage its state.
    '''

    def __init__(self, name : str): 
        self._name = name
        self._height = 0.1                      # ex : 50x50x10cm robot -- w=1.5kg
        self._lenght = 0.5
        self._weight = 1.5
        self._battery = 100.0
        self._wheels = {                        # from 0 to 100% speed of the wheels
            "front_right" : 0.0,
            "front_left" : 0.0,
            #"back_right" : 0.0,
            #"back_left" : 0.0
        }
        self._sensors = {
            "distance_array" : [0.0, 0.0, 0.0],    # left, center right
            #"bumper" : 0,                          # ex : turtlebot 
            #"image" : None,                        # camera
            #"depth_sensor" : None,                 # infra-rouge par ex 
        }

    def __repr__(self):
        return f"I am {self._name}, reading {self._sensors}"


    def get_battery(self):
        '''get battery state '''
        return self._battery

    def get_wheels(self):
        '''get wheels state '''
        return self._wheels

    def get_sensors(self):
        '''get sensors values '''
        return self._sensors

    def set_battery(self, value : int):
        '''set battery state '''
        self._battery = value
        return self._battery

    def set_wheels(self, tab : float):
        '''set wheels speed '''
        self._wheels["front_right"]=tab[0]
        self._wheels["front_left"]=tab[1]
        return self._wheels
    
    def set_sensors(self, sensors : s.Sensor):
        '''set sensors'''
        for sens in sensors:
            if sens.get_type() == "Lidar":
                if sens.get_name().find("0") !=-1:
                    self._sensors["distance_array"][0] = sens.get_value()
                elif sens.get_name().find("1") != -1:
                    self._sensors["distance_array"][1] = sens.get_value()
                elif sens.get_name().find("2") != -1:
                    self._sensors["distance_array"][2] = sens.get_value()
            else : 
                print("Mauvais capteur")
        return self._sensors


if __name__ == "__main__":
    r1=Robot("Data")
    print(r1)

    
''' test set values
    s0=s.Sensor("S0", "Lidar")
    s1=s.Sensor("S1", "Lidar")
    s2=s.Sensor("S2", "Lidar")
    s0.set_range([-1.0, 0.0])
    s1.set_range([0.0, 0.5])
    s2.set_range([0.5, 2.0])
    s0.set_value(-0.2)
    s1.set_value(0.1)
    s2.set_value(1.2)

    tab = [s0, s1, s2]
    r1.set_sensors(tab)
'''
