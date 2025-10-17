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
        self.left_wheel_speed = 0.0   # vitesse roue gauche [0, 1]
        self.right_wheel_speed = 0.0  # vitesse roue droite [0, 1]

    def __repr__(self):
        pass

    def execute(self, instructions):
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
                print(f"[WARNING] Action inconnue : {action_type}")

    def move_forward(self, duration, speed=1.0):
        self.left_wheel_speed = speed
        self.right_wheel_speed = speed

        # déplacement selon orientation
        dx = round(math.cos(math.radians(self.orientation)) * speed * duration)
        dy = round(math.sin(math.radians(self.orientation)) * speed * duration)

        self.robot._pos["x"] = max(0, min(self.environment["map_size"][0]-1, self.robot._pos["x"] + dx))
        self.robot._pos["y"] = max(0, min(self.environment["map_size"][1]-1, self.robot._pos["y"] + dy))

        # consommation batterie
        self.robot.battery = max(0, self.robot.get_battery() - duration / 5.0)
        print(f"Avance {duration}s à vitesse {speed} → pos=({self.robot._pos["x"]},{self.robot._pos["y"]}), batterie={self.robot.get_battery():.1f}%")

    def turn_left(self, duration, speed=1.0):
        self.left_wheel_speed = -speed
        self.right_wheel_speed = speed
        self.orientation = (self.orientation + 90 * duration) % 360
        self.robot.set_battery(max(0, self.robot.get_battery() - duration / 5.0))
        print(f"Tourne à gauche {duration}s → orientation={self.orientation}°, batterie={self.robot.get_battery():.1f}%")

    def turn_right(self, duration, speed=1.0):
        self.left_wheel_speed = speed
        self.right_wheel_speed = -speed
        self.orientation = (self.orientation - 90 * duration) % 360
        self.robot.set_battery(max(0, self.robot.get_battery() - duration / 5.0))
        print(f"Tourne à gauche {duration}s → orientation={self.orientation}°, batterie={self.robot.get_battery():.1f}%")

    def move_to(self, target):
        # déplacement 1 unité/sec simple
        tx, ty = target
        while (self.robot._pos["x"], self.robot._pos["y"]) != (tx, ty) and self.robot.get_battery() > 0:
            dx = 1 if tx > self.robot._pos["x"] else -1 if tx < self.robot._pos["x"] else 0
            dy = 1 if ty > self.robot._pos["y"] else -1 if ty < self.robot._pos["y"] else 0
            self.robot._pos["x"] += dx
            self.robot._pos["y"] += dy

            # Batterie : 1% / 5 sec → durée 1 sec par pas
            self.robot.set_battery(max(0, self.robot.get_battery() - 1.0 / 5.0))
            print(f"Moving to {target} → pos=({self.robot._pos["x"]},{self.robot._pos["y"]}), batterie={self.robot.get_battery():.1f}%")

    def recharge(self, duration):
        # Recharge 1% / sec
        self.robot.set_battery(min(100, self.robot.get_battery() + duration))
        print(f"Recharge {duration}s → batterie={self.robot.get_battery():.1f}%")

if __name__ == "__main__":
    pass
