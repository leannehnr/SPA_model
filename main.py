'''
SENSE PLAN ACT Simple Python <implementation
using 00P-classes 
'''
from .robot import robot as r
from .sense import sense as s
from .plan import plan as p
from .action import action as a

class Environment:
    """ Définition de l'environnement """
    def __init__(self, robot, obstacles):
        self._size = [10.0, 10.0]                               # taille de la zone à explorer
        self._recharge_zone = [(-0.5, 0.5), (-0.5, 0.5)]        # zone de recharge (xmin xmax), (ymin, ymax)
        self._init_pos = [0.0, 0.0]                             # position initale
        self._robot = robot                                     # robot
        self._nogo = obstacles                                  # obstacles -- none at the beginning
    
    def __repr__(self):
        pass

def main():
    print("Hello from spa-model!")
    turtle = r.Robot("Turtle")
    # Ajout des sensors
    environment = Environment(turtle, None)


if __name__ == "__main__":
    main()
