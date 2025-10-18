'''
Planner interface
'''
import random
from collections import deque

class Plan:
    '''
    Class that implement the planner interface
    Planner Class: This class will handle the planning aspect. It should have:

    Methods to process sensor data and make decisions.
    Algorithms for pathfinding or decision-making.
    '''

    def __init__(self, robot, environnement):
        self._action = {
            "move_to": (0.0, 0.0),        # move forward for x seconds
            "turn_right": 0.0,          # turn_right for x seconds
            "turn_left": 0.0,           # turn_left
            "slower" : 0.0,             # ralentir
            "faster" : 0.0,
            "recharge":0.0,             # wait until battery is full
            "collect":0.0,              # collect some reward ? 
        }
        self._goals = {                 # Prioritised goals (0-5)
            "life" : 0.0,               # first
            "exploration" : 2.0,        # second
            "finding_objects" : 5.0     # last
        }
        self._instruction = ["move"]          # list of instructions
        self.low_battery_threshold = 20
        self._start_pos = (0.0, 0.0)
        self._width = 10
        self._height = 10
        self._visited = set()
        self._env = environnement
        self._goal = (random.randint(0,9),random.randint(0,9))
        self.robot = robot

    def __repr__(self):
        return f"<Plan goals={self._goals}, next={self._instruction}>"


    def decide(self, perception):
        x, y = perception["position"]
        battery = perception["battery"]
        xr, yr = self._env["recharge_zone"]

        # Ajouter la case actuelle aux visités
        self._visited.add((x, y))
        exploration = len(self._visited)/(self._width*self._height - len(self._env["obstacles"]))*100
        print(f"Exploration : {exploration}%")
        # --- 1. Batterie faible ? retour à la base ---
        if battery < self.low_battery_threshold and (x,y)!=(xr,yr):
            self._instruction.append("move")
            return self.go_recharge((x,y), self._env["recharge_zone"])
        elif battery < self.low_battery_threshold and (x,y)==(xr,yr):
            self._instruction.append("charge")
            return self.recharge(perception)
        elif self._instruction[-1]=="charge" and battery<100:
            self._instruction.append("charge")
            return self.recharge(perception)

        # --- 2. Choisir la prochaine case à explorer ---
        next_cell = self.find_next_cell(x, y, perception)
        if next_cell and exploration<80:  #exploration
            self._instruction.append("move")
            return [("move_to", next_cell)]
        else:
            self._instruction.append("move")
            if (x,y)==self._goal or (x, y) in self._env["obstacles"]:
                self._goal = (random.randint(0,9),random.randint(0,9))
            return self.go_recharge((x,y), self._goal)

    def find_next_cell(self, x, y, perception):
        """
        Stratégie :
        - Avancer dans l'orientation actuelle si la case devant est libre et non visitée
        - Sinon, regarder droite/gauche pour trouver une case libre et non visitée
        - Si toutes les cases autour sont bloquées, reculer et marquer la case devant comme obstacle
        """
        move = 0
        front = perception["lidar_front"]
        left = perception["lidar_left"]
        right = perception["lidar_right"]
        move_front = (0, 0)
        move_left = (0, 0)
        move_back = (0, 0)
        move_right = (0, 0)

        if self.robot._orientation == 0:  # droite
            move_front = (x+1, y)
            move_left  = (x, y-1)
            move_right = (x, y+1)
            move_back = (x-1, y)
        elif self.robot._orientation == 180:  # gauche
            move_front = (x-1, y)
            move_left  = (x, y+1)
            move_right = (x, y-1)
            move_back = (x+1, y)
        elif self.robot._orientation == 90:  # haut
            move_front = (x, y-1)
            move_left  = (x-1, y)
            move_right = (x+1, y)
            move_back = (x, y+1)
        elif self.robot._orientation == 270:  # bas
            move_front = (x, y+1)
            move_left  = (x+1, y)
            move_right = (x-1, y)
            move_back = (x, y-1)

        # Priorisier d'aller sur une case qui n'a pas été visitée plutôt qu'une case visitée
        if front == 1.0 and move_front not in self._visited: # pas d'obstacle devant et ajouter la case devant n'a pas été visitée
            move = move_front
        elif left == 1.0 and move_left not in self._visited: # si obstacle devant, mais pas à gauche et que la case n'a pas été visitée
            move = move_left
            self.robot._orientation = (self.robot._orientation + 90) % 360
        elif right == 1.0 and move_right not in self._visited:
            move = move_right
            self.robot._orientation = (self.robot._orientation - 90) % 360
        elif front == 1.0:
            move = move_front
        elif right == 1.0:
            move = move_right
            self.robot._orientation = (self.robot._orientation - 90) % 360
        elif left == 1.0:
            move = move_left
            self.robot._orientation = (self.robot._orientation + 90) % 360
        else : # voie sans issue --> reculer
            move = move_back
            # marquer la case comme danger

        return move


    def explore(self):
        """
        Exploration aléatoire — pour l’instant, choix d’une direction au hasard.
        """
        actions = ["move_forward", "turn_left", "turn_right"]
        action = random.choice(actions)
        duration = round(random.uniform(0.5, 2.0), 2)
        self._action[action] = duration
        return [(action, duration)]


    def go_recharge(self, current_pos, goal):
        """
        Calcule un chemin vers la position 'goal' en évitant les obstacles.
        Se déplace uniquement horizontalement ou verticalement (pas de diagonales).
        Renvoie la prochaine position sûre à atteindre.
        """
        width, height = self._env["map_size"]
        obstacles = self._env.get("obstacles", set())
        start = current_pos

        # Si déjà sur place
        if start == goal:
            print(f"Already at {goal}")
            return [("move_to", goal)]

        # --- BFS pour trouver le chemin le plus court ---
        queue = deque([(start, [])])
        visited = {start}

        while queue:
            (x, y), path = queue.popleft()

            # Directions : droite, gauche, bas, haut
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                # Vérification des limites et obstacles
                if (0 <= nx < width and 0 <= ny < height
                    and next_pos not in obstacles
                    and next_pos not in visited):

                    # Si c'est la destination
                    if next_pos == goal:
                        full_path = path + [next_pos]
                        next_step = full_path[0] if full_path else goal
                        print(f"{start} vers {next_step} (objectif {goal})")
                        return [("move_to", next_step)]


                    queue.append((next_pos,path + [next_pos]))
                    visited.add(next_pos)

        # Si aucun chemin trouvé, on reste en place
        print(f"Aucun chemin trouvé vers {goal}, robot reste sur {current_pos}")
        return [("move_to", current_pos)]

    
    def recharge(self, perception):
        return [("recharge", 100-perception["battery"])]


if __name__ == "__main__":
    print("Testing functions")

