'''
Sensor interface
'''

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
    
    def set_range(self, values : float):
        if len(values)==2:
            self._range[0] = min(values)
            self._range[1] = max(values)
        return self._range
    
    def collect_data(self):
        if(self._type == "lidar"):
            pass
        elif(self._type == "video"):
            pass
        elif(self._type == "depth_sensor"):
            pass
        elif(self._type == "bumper"):
            pass
        else :
            print("Capteur inconnu")

if __name__ == "__main__":
    s1=Sensor("L1", "Lidar")
    print(s1)
    s1.collect_data()
