import pygame
import os 
import random
from objects import Object
from boids import Boids


## Defining some constants 
FPS = 120
WIDTH, HEIGHT = 1200, 900

## Initialize Pygame
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

## Load images
bird = pygame.image.load(os.path.join('Assets', 'fishhh.png'))
SPACE1 = pygame.image.load(os.path.join('Assets', 'the11.jpg'))

## Resize images 
bird_WIDTH, bird_HEIGHT = int(bird.get_width() * 0.2), int(bird.get_height() * 0.2)
bird1 = pygame.transform.scale(bird, (bird_WIDTH, bird_HEIGHT))
#bird1 = pygame.transform.rotate(bird1, 90)
SPACE = pygame.transform.scale(SPACE1, (WIDTH, HEIGHT))

## Create boids
boids = []
for i in range(50):
    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)
    boids.append(Boids(x, y, bird1, WIDTH, HEIGHT, boids))

# Setting the speed of the while-loop
clock = pygame.time.Clock() 

## Game loop
while True: 
    clock.tick(FPS)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break

    ## Move the boids
    for boid in boids:
        boid.update(WIDTH, HEIGHT)

    ## Draw the boids and the background
    WIN.blit(SPACE, (0,0))
    for boid in boids:
        boid.draw(WIN)

    pygame.display.update()

## Quit Pygame and exit
pygame.quit()
exit()
