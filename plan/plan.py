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
            "move_to": (0.0, 0.0),        # move to point (x, y)
            "recharge":0.0,             # wait until battery is full
            "collect":0.0,              # collect some reward ? / not used
            "move_forward" : 0.0, 
            "turn_left" : 0.0, 
            "turn_right" : 0.0
        }
        self._goals = {                 # Prioritised goals (0-5) / not used but still are the goals 
            "life" : 0.0,               # first
            "exploration" : 2.0,        # second
            "finding_objects" : 5.0     # last
        }
        self._instruction = [self._action["move_to"]]          # list of instructions / used as memory of actions
        self.low_battery_threshold = 20                        # when the robot go recharge
        self._start_pos = (0.0, 0.0)                           # starting position
        self._env = environnement                              # for the map size / the recharge zone / obstacles (at the end of the exploration part)
        self._width, self._height = self._env["map_size"]
        self._visited = set()                                  # visited area
        self._goal = (random.randint(0,self._width-1),random.randint(0,self._height-1)) # random goal positions at the end of the exploration
        self.robot = robot

    def __repr__(self):
        return f"<next={self._instruction}>"


    def decide(self, perception):
        """
        Decide what to do between explore, recharge and go recharge / move to random goal(same function)
        """
        x, y = perception["position"]
        battery = perception["battery"]
        xr, yr = self._env["recharge_zone"]

        # Add the actual pos to the visited cases
        self._visited.add((x, y))
        exploration = len(self._visited)/(self._width*self._height - len(self._env["obstacles"]))*100       # exploration rate
        print(f"Exploration : {exploration}%")
        # --- 1. Low battery ? go to recharge base ---
        if battery < self.low_battery_threshold and (x,y)!=(xr,yr): # still not on the base
            self._instruction.append("move")
            return self.go_recharge((x,y), (xr, yr))
        elif battery < self.low_battery_threshold and (x,y)==(xr,yr):   # start recharging
            self._instruction.append("charge")
            return self.recharge(perception)
        elif self._instruction[-1]=="charge" and battery<100:           # charge not finished -- continue recharging
            self._instruction.append("charge")
            return self.recharge(perception)

        # --- 2. Find somewhere to go ---
        next_cell = self.find_next_cell(x, y, perception)
        if next_cell and exploration<80:  # exploration
            self._instruction.append("move")
            return [("move_to", next_cell)]
        else:                             # and of the ex^ploration part -- random positions to go
            self._instruction.append("move")
            if (x,y)==self._goal or (x, y) in self._env["obstacles"]:   # if at goal -- generate new goal
                self._goal = (random.randint(0,9),random.randint(0,9))
            return self.go_recharge((x,y), self._goal)                  # find a path to the new goal

    def find_next_cell(self, x, y, perception):
        """
        - Know the actual position/orientation
        - Look around, if no obstacle in front -- go straight, else turn with prioritized instructions
        """
        move = 0
        front = perception["lidar_front"]
        left = perception["lidar_left"]
        right = perception["lidar_right"]
        move_front = (0, 0)
        move_left = (0, 0)
        move_back = (0, 0)
        move_right = (0, 0)

        if self.robot._orientation == 0:  # find where is the front give the orientation ( same in Sense ) and define the move 
            move_front = (x+1, y)
            move_left  = (x, y-1)
            move_right = (x, y+1)
            move_back = (x-1, y)
        elif self.robot._orientation == 180:
            move_front = (x-1, y)
            move_left  = (x, y+1)
            move_right = (x, y-1)
            move_back = (x+1, y)
        elif self.robot._orientation == 90:
            move_front = (x, y-1)
            move_left  = (x-1, y)
            move_right = (x+1, y)
            move_back = (x, y+1)
        elif self.robot._orientation == 270:
            move_front = (x, y+1)
            move_left  = (x+1, y)
            move_right = (x-1, y)
            move_back = (x, y-1)

        # Always prefer to go somewhere unknown
        if front == 1.0 and move_front not in self._visited: # nothing in front and not visited
            move = move_front
        elif left == 1.0 and move_left not in self._visited: # something or visited in front, turn left if left not visited and no obstacle
            move = move_left
            self.robot._orientation = (self.robot._orientation + 90) % 360
        elif right == 1.0 and move_right not in self._visited: # something or visited in front and left, turn right if right not visited and no obstacle 
            move = move_right
            self.robot._orientation = (self.robot._orientation - 90) % 360
        elif front == 1.0:  # if all around visited but nothing in front go straight
            move = move_front
        elif right == 1.0: # if all around visited and obstacle in front but nothing on the right go right
            move = move_right
            self.robot._orientation = (self.robot._orientation - 90) % 360
        elif left == 1.0: # if all around visited and obstacle in front and on the right but nothing on the left go left
            move = move_left
            self.robot._orientation = (self.robot._orientation + 90) % 360
        else : # move back
            move = move_back
        return move


    def explore(self):
        """
        Random exploration -- not used anymore
        """
        actions = ["move_forward", "turn_left", "turn_right"]
        action = random.choice(actions)
        duration = round(random.uniform(0.5, 2.0), 2)
        self._action[action] = duration
        return [(action, duration)]


    def go_recharge(self, current_pos, goal):
        """
        Compute the shortest path to the goal while do run over obstacles
        """
        width, height = self._env["map_size"]
        obstacles = self._env.get("obstacles", set())
        start = current_pos

        # Si déjà sur place
        if start == goal:
            print(f"Already at {goal}")
            return [("move_to", goal)]

        # --- BFS (Breadth-First Search) to find the shortest path ---
        queue = deque([(start, [])])
        visited = {start}

        while queue:
            (x, y), path = queue.popleft()

            # Directions : right, left, up, down
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                # Limits of the grid and obstacles
                if (0 <= nx < width and 0 <= ny < height
                    and next_pos not in obstacles
                    and next_pos not in visited):

                    # If destination found
                    if next_pos == goal:
                        full_path = path + [next_pos]
                        next_step = full_path[0] if full_path else goal
                        print(f"{start} vers {next_step} (objectif {goal})")
                        return [("move_to", next_step)]


                    queue.append((next_pos,path + [next_pos]))
                    visited.add(next_pos)

        # if no path found -- not supposed to arrive
        print(f"Aucun chemin trouvé vers {goal}, robot reste sur {current_pos}")
        return [("move_to", current_pos)]

    # send the recharge instruction
    def recharge(self, perception):
        return [("recharge", 100-perception["battery"])]


if __name__ == "__main__":
    print("Testing functions")
