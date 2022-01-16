# Import the pygame module
import pygame
import random
import time
import numpy as np
import math

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

# Define constants for the screen width and height
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

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Player_left(pygame.sprite.Sprite):
    def __init__(self):
        super(Player_left, self).__init__()
        self.surf = pygame.Surface((20,100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (10,300))

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)

        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#player_size = input('Enter sprite size:')
#player_size = tuple((int(i) for i in player_size.split()))


# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player_right = Player_right()
player_left = Player_left()
player_left_score = 0
player_right_score = 0
circle_x = 400
circle_y = 300
ranges = [(1/24,1/12), (5/12,7/12), (11/12,23/24)]
random_int = random.randrange(3)
r = random.uniform(*ranges[random_int])
ball_angle = np.pi * 2 * r
ball_x_direction_original = 8 * np.cos(ball_angle)
ball_y_direction_original = 8 * np.sin(ball_angle)

if np.sign(ball_x_direction_original) >= 0:
    ball_x_direction_original = math.ceil(ball_x_direction_original)
else:
    ball_x_direction_original = math.floor(ball_x_direction_original)

if np.sign(ball_y_direction_original) >= 0:
    ball_y_direction_original = math.ceil(ball_y_direction_original)
else:
    ball_y_direction_original = math.floor(ball_y_direction_original)

# Variable to keep the main loop running
running = True

right_through = True
left_through = True

# Main loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
               running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

    # Draw the player on the screen
    screen.blit(player_right.surf, player_right.rect)
    screen.blit(player_left.surf, player_left.rect)
    pygame.draw.circle(screen, (255,255,255), (circle_x,circle_y), 10)

    pressed_keys = pygame.key.get_pressed()
    circle_x += ball_x_direction_original
    circle_y += ball_y_direction_original
    circle_x = int(circle_x)
    circle_y = int(circle_y)

    #Make the ball bounce off the top of the screen
    if circle_y - 10 < 0:
        circle_y = 10
        ball_y_direction_original = -1.05*ball_y_direction_original


    #Make the ball bounce off the top of the screen
    if circle_y + 10 >= 600:
        ball_y_direction_original = -1.05*ball_y_direction_original


    #Make the ball bounce off the left player when appropriate and adjust the score
    if (circle_x - 10 <= 20 and player_left.rect.top > circle_y + 10) or (circle_x - 10 <= 20 and player_left.rect.bottom < circle_y - 10):
        player_right_score += 1
        print('P2 score is: ' + str(player_right_score))
        circle_x = 400
        circle_y = 300

        ranges = [(1/24,1/12), (5/12,7/12), (11/12,23/24)]
        random_int = random.randrange(3)
        r = random.uniform(*ranges[random_int])
        ball_angle = np.pi * 2 * r
        ball_x_direction_original = 5 * np.cos(ball_angle)
        ball_y_direction_original = 5 * np.sin(ball_angle)

        if np.sign(ball_x_direction_original) >= 0:
            ball_x_direction_original = math.ceil(ball_x_direction_original)
        else:
            ball_x_direction_original = math.floor(ball_x_direction_original)

        if np.sign(ball_y_direction_original) >= 0:
            ball_y_direction_original = math.ceil(ball_y_direction_original)
        else:
            ball_y_direction_original = math.floor(ball_y_direction_original)

    elif circle_y - 10 <= player_left.rect.bottom and circle_y + 10 >= player_left.rect.top:
        if circle_x - 10 < 20:
            circle_x = 20
            ball_x_direction_original = -1.04*ball_x_direction_original

    #Make the ball bounce off the right player when appropriate and adjust the score
    if (circle_x + 10 >= 780 and player_right.rect.top > circle_y + 10) or (circle_x + 10 >= 780 and player_right.rect.bottom < circle_y - 10):
        player_left_score += 1
        print('P1 score is: ' + str(player_left_score))
        circle_x = 400
        circle_y = 300

        ranges = [(1/24,1/12), (5/12,7/12), (11/12,23/24)]
        random_int = random.randrange(3)
        r = random.uniform(*ranges[random_int])
        ball_angle = np.pi * 2 * r
        ball_x_direction_original = 5 * np.cos(ball_angle)
        ball_y_direction_original = 5 * np.sin(ball_angle)

        if np.sign(ball_x_direction_original) >= 0:
            ball_x_direction_original = math.ceil(ball_x_direction_original)
        else:
            ball_x_direction_original = math.floor(ball_x_direction_original)

        if np.sign(ball_y_direction_original) >= 0:
            ball_y_direction_original = math.ceil(ball_y_direction_original)
        else:
            ball_y_direction_original = math.floor(ball_y_direction_original)


    elif circle_y - 10 <= player_right.rect.bottom and circle_y + 10 >= player_right.rect.top:
        if circle_x + 10 > 780:
            circle_x = 780
            ball_x_direction_original = -1.04*ball_x_direction_original


    player_right.update(pressed_keys)
    player_left.update(pressed_keys)
    pygame.display.flip()

    # Fill the screen with black
    screen.fill((0, 0, 0))
    
