## NEAT-PONG
Using NEAT-Python to train pong

## The Files
We use the NEAT-python package to train a homemade version of Pong.

pong_game.py -- This is a version of the game in which two players can battle.

pong_training_right.py -- This uses NEAT to train an AI playing on the right side of the screen.

config-feedforward.txt -- The config file with the parameters NEAT requires. It is necessary for pong_training_right.py to work.

pong_vs_AI.py -- This is a version of the game in which the player controls the left side, and the right side is controlled by the FFNN from NEAT. (needs to be coded)

## Acknowledgements
This project relied heavily on content and teaching from TechWithTim. His youtube series on using NEAT to train a flappy bird game can be found here: https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2. His github for the flappy bird project can be found at https://github.com/techwithtim/NEAT-Flappy-Bird.

The config file was essentially copy and pasted from TechWithTim. For an explanation of what the parameters are, refer to either the resources from TechWithTim, or to the NEAT documentation, found here: https://neat-python.readthedocs.io/en/latest/config_file.html
