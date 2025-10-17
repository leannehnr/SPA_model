'''
Planner interface
'''
import random 

class Plan:
    '''
    Class that implement the planner interface
    Planner Class: This class will handle the planning aspect. It should have:

    Methods to process sensor data and make decisions.
    Algorithms for pathfinding or decision-making.
    '''

    def __init__(self):
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
        self._instruction = []          # list of instructions
        self.low_battery_threshold = 20
        self._start_pos = (0.0, 0.0)
        self._width = 10
        self._height = 10
        self._visited = set()

    def __repr__(self):
        return f"<Plan goals={self._goals}, next={self._instruction}>"


    def decide(self, perception):
        x, y = perception["position"]
        battery = perception["battery"]
        obstacle = perception["obstacle_ahead"]

        # Ajouter la case actuelle aux visités
        self._visited.add((x, y))

        # --- 1. Batterie faible ? retour à la base ---
        if battery < self.low_battery_threshold:
            return self.go_recharge((x,y))

        # --- 2. Obstacle détecté ? tourner ---
        if obstacle:
            return [("turn_left", 1.0)]

        # --- 3. Choisir la prochaine case à explorer ---
        next_cell = self.find_next_cell(x, y)
        if next_cell:
            return [("move_to", next_cell)]
        else:
            # Tout exploré, rester sur place
            return [("move_forward", 1.0)]

    def find_next_cell(self, x, y):
        """
        Choisir la prochaine case non visitée dans la grille.
        Stratégie : balayage ligne par ligne (zig-zag)
        """
        # Déterminer la direction de la ligne actuelle
        row = y
        if row % 2 == 0:
            # Ligne pair → aller vers la droite
            for nx in range(x+1, self._width):
                if (nx, row) not in self._visited:
                    return (nx, row)
            # Fin de ligne → descendre si possible
            if row + 1 < self._height:
                return (self._width-1, row+1)
        else:
            # Ligne impair → aller vers la gauche
            for nx in range(x-1, -1, -1):
                if (nx, row) not in self._visited:
                    return (nx, row)
            if row + 1 < self._height:
                return (0, row+1)
        # Si aucune case disponible
        return None
    

    def explore(self):
        """
        Exploration aléatoire — pour l’instant, choix d’une direction au hasard.
        """
        actions = ["move_forward", "turn_left", "turn_right"]
        action = random.choice(actions)
        duration = round(random.uniform(0.5, 2.0), 2)
        self._action[action] = duration
        return [(action, duration)]
    
    def go_recharge(self, current_pos):
        """
        Retour progressif vers la base (0,0) en se déplaçant uniquement
        horizontalement ou verticalement (pas de diagonale).
        """
        x, y = current_pos
        if x > 0:
            next_pos = (x - 1, y)   # avancer vers la gauche
        elif y > 0:
            next_pos = (x, y - 1)   # avancer vers le haut
        else:
            next_pos = (0, 0)       # déjà arrivé

        return [("move_to", next_pos)]


if __name__ == "__main__":
    print("Testing functions")
    p1=Plan()

