'''
Physical robot interface
'''

class Robot: 
    '''
    Class that implement the physical robot interface

    This will be the main class that represents the robot. It should contain:

    Attributes for the robot's body (e.g., size, weight, battery level).
    Methods to initialize the robot and manage its state.
    '''

    def __init__(self, name : str): 
        self._name = name
        self._wheels = {
            "front_right" : 0.0,
            "front_left" : 0.0,
            "back_right" : 0.0,
            "back_left" : 0.0
        }
        self._sensors = {
            "distance_array" : [0.0, 0.0, 0.0], # left, center right
            "battery":0.0
            #...
        }

    def __repr__(self):
        return f"I am {self._name}, reading {self._sensors}"

if __name__ == "__main__": 
    r1=Robot("Data")
    print(r1)