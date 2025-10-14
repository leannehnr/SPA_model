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
        self._range = [(), ()]  #tuple min, tuple max --> polar coordinates more than 1 limit -- à voir
        self._value = []       # mettre un tableau de valeurs - si il y en a qu'une chill

    def __repr__(self):
        return f"I am {self._name}, reading {self._value}"

if __name__ == "__main__":
    s1=Sensor("L1", "Lidar")
    print(s1)
