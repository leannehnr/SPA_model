# SPA Model
## Quick description 
Sense - Plan - Act d'un module mobile. Simulation d'un environnement dans lequel il ne peut se déplacer que case par case (pas en diagonale). L'environnement comporte des obstacles que le robot ne connait pas au départ et qu'il doit "détecter" grace à ses capteurs. Si un obstacle est sur une case à coté d'un capteur (lidar), ce dernier le détecte et l'indique au robot. De cette façon il ne cherche pas à traverser l'obstacle. 

Son objectif est d'explorer 80% de la zone sans se décharger. Ensuite il reçoit des positions aléatoires auxquelles se déplacer pour finir son exploration. Il connaît toujours la position de sa zone de recharge. Une fois que la batterie est inférieure à 20% il plannifie un chemin jusqu'à sa zone de recharge et y reste jusqu'à la fin du chargement. 


## How to use 
```pip install requirements.txt```

``python -m SPA_model.main``