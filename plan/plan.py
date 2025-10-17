'''
Planner interface
'''

import time


class Plan:
    '''
    Class that implement the planner interface
    Planner Class: This class will handle the planning aspect. It should have:

    Methods to process sensor data and make decisions.
    Algorithms for pathfinding or decision-making.
    '''

    def __init__(self):
        self._action = {
            "move_forward": 0.0,        # move forward for x seconds
            "move_backward": 0.0,       # move backward for x seconds
            "turn_right": 0.0,          # turn_right for x seconds
            "turn_left": 0.0,           # turn_left
            "slower" : 0.0,             # ralentir
            "faster" : 0.0,
            "recharge":0.0,             # recharge until battery is full
            "collect":0.0,              # collect some reward ? 
        }
        self._goals = {                 # Prioritised goals (0-5)
            "life" : 0.0,               # first
            "exploration" : 2.0,        # second
            "finding_objects" : 5.0     # last
        }
        self._instruction = []          # list of instructions

    def __repr__(self):
        pass
    
    # find the shorter path to the recharge zone 
    def go_recharge(self):
        pass

    # recharge 100-battery rate seconds
    def recharging(self):
        while(self._action.get("recharge") > 0.0):
            print ("recharging...")
            time.sleep(1)
            self._action["recharge"] -= 1
        print("Battery is full.")

    # explore the environment / when going somehere it never had been --> reward / only the plan
    def explore(self): 
        pass

if __name__ == "__main__":
    print("Testing functions")
    p1=Plan()
    p1.recharging()

