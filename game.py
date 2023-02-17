import pygame
import pygame_gui
import os 
import random
from boids import Boids
from button import ToggleButton

## Defining some constants 
FPS = 120
WIDTH, HEIGHT = 1200, 900

# Initialize Pygame
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Boids')

## Load images
bird = pygame.image.load(os.path.join('Assets', 'trigy.png'))
SPACE1 = pygame.image.load(os.path.join('Assets', 'the11.jpg'))

## Resize images 
bird_WIDTH, bird_HEIGHT = int(bird.get_width() * 0.1), int(bird.get_height() * 0.1)
bird1 = pygame.transform.scale(bird, (bird_WIDTH, bird_HEIGHT))
SPACE = pygame.transform.scale(SPACE1, (WIDTH, HEIGHT))

## Create the borders
border_thickness = 25
border = pygame.Surface((WIDTH, border_thickness))
border.fill((100,150,110))



separation_button = ToggleButton(
    x=WIDTH - 220,
    y=100,
    width=200,
    height=50,
    on_text='Separation: On',
    off_text='Separation: Off',
    font=pygame.font.Font(None, 24),
    on_color=(0, 255, 0),
    off_color=(255, 0, 0),
    screen=WIN,
    initial_state=True
)

cohesion_button = ToggleButton(
    x=WIDTH - 220,
    y=170,
    width=200,
    height=50,
    on_text='Cohesion: On',
    off_text='Cohesion: Off',
    font=pygame.font.Font(None, 24),
    on_color=(0, 255, 0),
    off_color=(255, 0, 0),
    screen=WIN,
    initial_state=True
)

alignment_button = ToggleButton(
    x=WIDTH - 220,
    y=240,
    width=200,
    height=50,
    on_text='Alignment: On',
    off_text='Alignment: Off',
    font=pygame.font.Font(None, 24),
    on_color=(0, 255, 0),
    off_color=(255, 0, 0),
    screen=WIN,
    initial_state=True
)

def main():

    ## Create boids
    boids = []
    for i in range(100):
        x = random.randint(50,WIDTH-50)
        y = random.randint(20,HEIGHT-20)
        boids.append(Boids(x, y, bird1, WIDTH, HEIGHT, boids, border_thickness, True, True, True))

    # Setting the speed of the while-loop
    clock = pygame.time.Clock() 
    run = True
    ## Game loop
    while run: 
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            pos = pygame.mouse.get_pos()  # get the mouse position
            if separation_button.check_clicked(event, pos):
                for boid in boids:
                    boid.separation_on = separation_button.state
            if cohesion_button.check_clicked(event, pos):
                for boid in boids:
                    boid.cohesion_on = cohesion_button.state
            if alignment_button.check_clicked(event, pos):
                for boid in boids:
                    boid.alignment_on = alignment_button.state


        ## Move the boids
        for boid in boids:
            boid.update(WIDTH, HEIGHT)

        ## Draw the boids and the background
        WIN.blit(SPACE, (0,0))
        WIN.blit(border,(0,0))
        WIN.blit(border,(0,HEIGHT-border_thickness))
        for boid in boids:
            boid.draw(WIN)
        
        alignment_button.draw()
        separation_button.draw()
        cohesion_button.draw()


        pygame.display.update()


    ## Quit Pygame and exit
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()