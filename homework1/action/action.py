'''
Act interface
'''
import math
from ..sense import sense as s

class Action:
    '''
    Class that implement the act interface
    Actuator Class: Finally, create a class for the actuators. This class should include:

    Methods to perform actions based on the plan (e.g., move forward, turn).
    Attributes for different types of actuators (e.g., motors, servos).
    '''

    def __init__(self, robot, environment):
        self.robot = robot
        self.environment = environment
        self.orientation = 0  # orientation en degrés
        self.left_wheel_speed = 0.0   # vitesse roue gauche [-1, 1]
        self.right_wheel_speed = 0.0  # vitesse roue droite [-1, 1]

    def __repr__(self):
        pass

    def execute(self, instructions):
        """
        Read the instruction from the plan 
        """
        for instr in instructions:
            action_type = instr[0]

            # durée en secondes
            duration = instr[1] if len(instr) > 1 else 1.0

            if action_type == "move_forward":
                self.move_forward(duration)
            elif action_type == "turn_left":
                self.turn_left(duration)
            elif action_type == "turn_right":
                self.turn_right(duration)
            elif action_type == "move_to":
                target = instr[1]
                self.move_to(target)
            elif action_type == "recharge":
                self.recharge(duration)
            else:
                print(f"[WARNING] Unknown action : {action_type}")

    # Move forward, turn_left, turn_right --> only for v1 not used in final version 
    # Could be called in move_to
    def move_forward(self, duration, speed=1.0):
        self.left_wheel_speed = speed
        self.right_wheel_speed = speed

        # déplacement selon orientation
        dx = round(math.cos(math.radians(self.orientation)) * speed * duration)
        dy = round(math.sin(math.radians(self.orientation)) * speed * duration)

        self.robot._pos["x"] = max(0, min(self.environment["map_size"][0]-1, self.robot._pos["x"] + dx))
        self.robot._pos["y"] = max(0, min(self.environment["map_size"][1]-1, self.robot._pos["y"] + dy))

        # consommation batterie
        self.robot.battery = max(0, self.robot.get_battery() - duration / 2.0)
        print(f"Avance {duration}s à vitesse {speed} → pos=({self.robot._pos["x"]},{self.robot._pos["y"]}), batterie={self.robot.get_battery():.1f}%")

    def turn_left(self, duration, speed=1.0):
        self.left_wheel_speed = -speed
        self.right_wheel_speed = speed
        self.orientation = (self.orientation + 90 * duration) % 360
        self.robot.set_battery(max(0, self.robot.get_battery() - duration / 2.0))
        print(f"Tourne à gauche {duration}s → orientation={self.orientation}°, batterie={self.robot.get_battery():.1f}%")

    def turn_right(self, duration, speed=1.0):
        self.left_wheel_speed = speed
        self.right_wheel_speed = -speed
        self.orientation = (self.orientation - 90 * duration) % 360
        self.robot.set_battery(max(0, self.robot.get_battery() - duration / 2.0))
        print(f"Tourne à gauche {duration}s → orientation={self.orientation}°, batterie={self.robot.get_battery():.1f}%")

    def move_to(self, target):
        tx, ty = target
        x, y = self.robot._pos["x"], self.robot._pos["y"]
        # Find if the robot has to turn 
        dx = tx - x
        dy = ty - y
        if dx > 0:
            desired_orientation = 0     # droite
        elif dx < 0:
            desired_orientation = 180   # gauche
        elif dy > 0:
            desired_orientation = 270   # bas
        elif dy < 0:
            desired_orientation = 90    # haut
        else:
            desired_orientation = self.robot._orientation
        # Turn
        if self.robot._orientation != desired_orientation:
            # Choisir le sens de rotation le plus court
            diff = (desired_orientation - self.robot._orientation) % 360
            if diff == 90 or diff == -270:
                self.robot._orientation = (self.robot._orientation + 90) % 360
            elif diff == 270 or diff == -90:
                self.robot._orientation = (self.robot._orientation - 90) % 360
            else:
                self.robot._orientation = desired_orientation
        # Move forward in the actual direction
        if self.robot._orientation == 0:
            self.robot._pos["x"] += 1
        elif self.robot._orientation == 180:
            self.robot._pos["x"] -= 1
        elif self.robot._orientation == 90:
            self.robot._pos["y"] -= 1
        elif self.robot._orientation == 270:
            self.robot._pos["y"] += 1
        # Stay in the grid (but shouldn't be a problem)
        width, height = self.environment["map_size"]
        self.robot._pos["x"] = max(0, min(self.robot._pos["x"], width-1))
        self.robot._pos["y"] = max(0, min(self.robot._pos["y"], height-1))

        # Batterie : -1% / 2 sec → 1sec / case
        self.robot.set_battery(max(0, self.robot.get_battery() - 1.0 / 2.0))
        print(f"batterie={self.robot.get_battery():.1f}%")

    def recharge(self, duration):
        # Recharge 1% / sec
        self.robot.set_battery(min(100, self.robot.get_battery() + 1))
        print(f"Recharge {duration}s → batterie={self.robot.get_battery():.1f}%")

if __name__ == "__main__":
    pass
