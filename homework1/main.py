'''
SENSE PLAN ACT Simple Python implementation
using 00P-classes 
'''
import sys
import pygame
from .robot import robot as r
from .sense import sense as s
from .plan import plan as p
from .action import action as a

# Paramètres
CELL_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 10
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

pygame.init() # pylint: disable=no-member
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SPA Robot Simulation")
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (SCREEN_WIDTH, y))

def draw_robot(robot):
    x, y = robot._pos["x"], robot._pos["y"]
    pygame.draw.circle(screen, (0, 100, 255), (x*CELL_SIZE + CELL_SIZE//2, y*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)

def draw_base(pos):
    x, y = pos
    pygame.draw.rect(screen, (0, 255, 0), (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_obs(pos):
    x, y = pos
    pygame.draw.rect(screen, (100, 0, 100), (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    turtle = r.Robot("Turtle")
    environment = {"map_size": (GRID_WIDTH,GRID_HEIGHT), "recharge_zone": (4,5), "obstacles": {(2, 3),(5, 5), (5, 8),(4, 9)}}
    sense = s.Sense(turtle, environment)
    planner = p.Plan(turtle, environment)
    actuator = a.Action(turtle, environment)

    running = True
    step = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # pylint: disable=no-member
                running = False

        # SPA cycle
        perception = sense.perceive()
        decision = planner.decide(perception)
        actuator.execute(decision)

        # Dessin
        screen.fill((255, 255, 255))
        draw_grid()
        draw_base(environment["recharge_zone"])
        obstacles = environment["obstacles"]
        for (x, y) in obstacles:
            draw_obs((x,y))
        draw_robot(turtle)
        pygame.display.flip()

        step += 1
        pygame.time.delay(500)

        
        if turtle.get_battery() <= 0:
            running = False

    pygame.quit() # pylint: disable=no-member
    sys.exit()

if __name__ == "__main__":
    main()