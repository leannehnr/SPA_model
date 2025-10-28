# SPA Model - Léanne Henry - ISRLAB 2025/2026
## Quick description (V1)
--> robot / sense / plan / act folders + main.py
Sense–Plan–Act model for a mobile module. 

This project simulates an environment where the robot can only move from cell to cell (no diagonal movement).
The environment contains unknown obstacles that the robot must detect using its sensors.
If an obstacle is located in a cell adjacent to a sensor (lidar), the sensor detects it and informs the robot, so it avoids trying to move through the obstacle.

The robot’s goal is to explore 80% of the area without running out of battery.After that, it receives random target positions to reach in order to complete its exploration. It always knows the position of its charging zone. Once the battery level drops below 20%, it plans a path back to the charging zone and stays there until it is fully recharged.

[WARNING] The area is supposed to be a square -- you can change the dimension but not the shape


## How to use 
Install the dependencies listed in requirements.txt :

``pip install -r requirements.txt``

Then, from the directory SPA_model, run :

```python -m homework1.main```