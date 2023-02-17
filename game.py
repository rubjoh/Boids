import pygame
import pygame_gui
import os 
import random
from boids import Boids


## Defining some constants 
FPS = 120
WIDTH, HEIGHT = 1200, 900

# Initialize Pygame
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

## Load images
bird = pygame.image.load(os.path.join('Assets', 'trigy.png'))
SPACE1 = pygame.image.load(os.path.join('Assets', 'the11.jpg'))

## Resize images 
bird_WIDTH, bird_HEIGHT = int(bird.get_width() * 0.1), int(bird.get_height() * 0.1)
bird1 = pygame.transform.scale(bird, (bird_WIDTH, bird_HEIGHT))
#bird1 = pygame.transform.rotate(bird1, 90)
SPACE = pygame.transform.scale(SPACE1, (WIDTH, HEIGHT))

## Create the borders
border_thickness = 25
border = pygame.Surface((WIDTH, border_thickness))
border.fill((100,150,110))

# Initialize GUI manager
gui = pygame_gui.UIManager((WIDTH,HEIGHT))

## Create a simple button
button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH/2 - 50, HEIGHT/2 - 25), (100, 50)),
    text='Hello',
    manager=gui
)

def main():

    ## Create boids
    boids = []
    for i in range(100):
        x = random.randint(50,WIDTH-50)
        y = random.randint(20,HEIGHT-20)
        boids.append(Boids(x, y, bird1, WIDTH, HEIGHT, boids, border_thickness))

    # Setting the speed of the while-loop
    clock = pygame.time.Clock() 

    ## Game loop
    while True: 
        clock.tick(FPS)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        ## Handle events for the GUI
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    print('Hello!')

        ## Update the GUI
        gui.process_events(event)
        gui.update(FPS/1000)

        ## Move the boids
        for boid in boids:
            boid.update(WIDTH, HEIGHT)

        ## Draw the boids and the background
        WIN.blit(SPACE, (0,0))
        WIN.blit(border,(0,0))
        WIN.blit(border,(0,HEIGHT-border_thickness))
        for boid in boids:
            boid.draw(WIN)
        ## Draw the GUI
        gui.draw_ui(WIN)

        pygame.display.update()


    ## Quit Pygame and exit
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()