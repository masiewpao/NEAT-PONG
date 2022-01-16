# Import the pygame module
import pygame
import random
import time
import numpy as np
import math
import neat 
import os
import visualize
import pickle

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_BACKSPACE,
    KEYDOWN,
    K_w,
    K_a,
    K_s,
    K_d,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player_right(pygame.sprite.Sprite):

    def __init__(self):
        super(Player_right, self).__init__()
        self.surf = pygame.Surface((20,100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (790,300))

    def move_up(self):
        self.rect.move_ip(0, -10)
        if self.rect.top <= 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.move_ip(0, 10)
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    # def update(self, pressed_keys):
    #     if pressed_keys[K_UP]:
    #         self.rect.move_ip(0, -5)

    #     if pressed_keys[K_DOWN]:
    #         self.rect.move_ip(0, 5)

    #     # # if self.rect.left < 0:
    #     # #     self.rect.left = 0

    #     # # if self.rect.right > SCREEN_WIDTH:
    #     # #     self.rect.right = SCREEN_WIDTH

    #     # if self.rect.top <= 0:
    #     #     self.rect.top = 0

    #     # if self.rect.bottom >= SCREEN_HEIGHT:
    #     #     self.rect.bottom = SCREEN_HEIGHT

    def collision(self,circle_x,circle_y):

        if circle_y - 10 <= self.rect.bottom and circle_y + 10 >= self.rect.top:
            if circle_x + 10 >= 780:
                circle_x = 780
                return True

class Wall_left(pygame.sprite.Sprite):

    def __init__(self):
        super(Wall_left, self).__init__()
        self.surf = pygame.Surface((20,600))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (10,300))

    def collision(self,circle_x,circle_y):
        if circle_x - 10 < 20:
            circle_x = 20
            return True

def draw_window(screen, players, circle_x, circle_y, wall):
    screen.fill((0, 0, 0))
    for i in players:
        screen.blit(i.surf,i.rect)

    screen.blit(wall.surf, wall.rect)

    pygame.draw.circle(screen, (255,255,255), (circle_x,circle_y), 10)

    pygame.display.flip()

# Initialize pygame


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT

# Variable to keep the main loop running


# Main loop
def eval_genomes(genomes, config):

    global circle_x, circle_y, ball_y_direction_original, ball_x_direction_original, running, wall_left, SCREEN_WIDTH, SCREEN_HEIGHT
    pygame.init()
    running = True
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Instantiate player. Right now, this is just a rectangle.
    wall_left = Wall_left()
    circle_x = 400
    circle_y = 300

    #Implement the random direction the ball will travel in
    ranges = [(1/24,1/12), (5/12,7/12), (11/12,23/24)]
    random_int = random.randrange(3)
    r = random.uniform(*ranges[random_int])
    ball_angle = np.pi * 2 * r
    ball_x_direction_original = 20 * np.cos(ball_angle)
    ball_y_direction_original = 20 * np.sin(ball_angle)
    print(ball_x_direction_original)

    if np.sign(ball_x_direction_original) >= 0:
        ball_x_direction_original = math.ceil(ball_x_direction_original)
    else:
        ball_x_direction_original = math.floor(ball_x_direction_original)

    if np.sign(ball_y_direction_original) >= 0:
        ball_y_direction_original = math.ceil(ball_y_direction_original)
    else:
        ball_y_direction_original = math.floor(ball_y_direction_original)

    nets =[]
    players_right = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        players_right.append(Player_right())
        ge.append(genome)

    circle_x += ball_x_direction_original
    circle_y += ball_y_direction_original
    circle_x = int(circle_x)
    circle_y = int(circle_y)
    players_right[0].move_up
    clock = pygame.time.Clock()
    #draw_window(screen, players_right, circle_x, circle_y, wall_left)
    #Make the ball bounce off the left player when appropriate and adjust the score
    while running and len(players_right) > 0:
        #clock.tick(10)

        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                   running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    running = False

        #MBounce off the top
        if circle_y - 10 < 0:
            circle_y = 10
            ball_y_direction_original = -ball_y_direction_original

        if circle_y + 10 >= 600:
            ball_y_direction_original = -ball_y_direction_original


        #Bounce off the left wall
        if wall_left.collision(circle_x,circle_y):
            ball_x_direction_original = -ball_x_direction_original


        #Iteration through the player objects
        players_remaining = len(players_right)
        should_bounce = False

        for j,i in enumerate(players_right):
            print('we are now in the for loop, looking at player number: ', j)


            #Add fitness whenever the player object is an element in players_right
            ge[j].fitness += 20

            #Neural netouput corresponding to the j-th player object
            output = nets[j].activate((circle_x,circle_y, ball_x_direction_original, ball_y_direction_original, i.surf.get_rect()[1]))

            #If the ball should bounce off of ANY of the player objects, we set it to bounce
            if i.collision(circle_x, circle_y):
                should_bounce = True
                # print('The player: ', j, ' has collided')
                # print('the current ball_x_driection is: ', ball_x_direction_original)
                # print('The bottom of the rect is: ', i.rect.bottom)
                # print('The top of the rect is: ', i.rect.top)
                # print('circle_x: ', circle_x)
                # print('circle_y: ', circle_y)

            #Behaviour depending on the output of the neural network associated with the j-th plater (i.e. associated with i)
            if output[0] > 0.8:
                i.move_up()
                pygame.display.flip()

            elif output[0] < 0.2:
                i.move_down()
                pygame.display.flip()


            #Determining whether the ball has passed the current player object (the current player object is i, which has index j)
            if (circle_x + 10 >= 780 and i.rect.top > circle_y + 10) or (circle_x + 10 >=780 and i.rect.bottom < circle_y - 10):
                #Before reomval, we reduce fitness of eliminated players
                ge[j].fitness += 10*abs(1/(circle_y - i.rect.center[1]))

                #We remove the player object i, the associated genome, and the assocaited neural network
                players_right.pop(j)
                ge.pop(j)
                nets.pop(j)

        if should_bounce:
            ball_x_direction_original = -ball_x_direction_original

        #If players_right isn't empty, then in the for loop above, at least one of the player objects was such that the ball should bounce
        circle_x += ball_x_direction_original
        circle_y += ball_y_direction_original
        circle_x = int(circle_x)
        circle_y = int(circle_y)

        draw_window(screen, players_right, circle_x, circle_y, wall_left)
    
def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
