import pygame
import pygame_gui
import os 
import random
from boids import Boids
from button import ToggleButton
from predator import Predator

## Defining some constants 
FPS = 120
WIDTH, HEIGHT = 1200, 900

# Initialize Pygame
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Boids')

## Load images
boid = pygame.image.load(os.path.join('Assets', 'trigy.png'))
SPACE1 = pygame.image.load(os.path.join('Assets', 'the11.jpg'))
predator = pygame.image.load(os.path.join('Assets', 'predator.png'))

## Resize images 
boid_WIDTH, boid_HEIGHT = int(boid.get_width() * 0.1), int(boid.get_height() * 0.1)
predator_WIDTH, predator_HEIGHT = int(predator.get_width() * 0.1), int(predator.get_height() * 0.1)
boid1 = pygame.transform.scale(boid, (boid_WIDTH, boid_HEIGHT))
predator1 = pygame.transform.scale(predator, (boid_WIDTH, boid_HEIGHT))
SPACE = pygame.transform.scale(SPACE1, (WIDTH, HEIGHT))

## Create the borders
border_thickness = 25
border = pygame.Surface((WIDTH, border_thickness))
border.fill((100,150,110))


## Define simple toggle buttons

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
    for i in range(50):
        x = random.randint(50,WIDTH-50)
        y = random.randint(20,HEIGHT-20)
        boids.append(Boids(x, y, boid1, WIDTH, HEIGHT, boids, border_thickness, True, True, True))

    ## Create predators
    predators = []
    for i in range(2):
        x = random.randint(50,WIDTH-50)
        y = random.randint(20,HEIGHT-20)
        predators.append(Predator(x, y, predator1, WIDTH, HEIGHT, boids, border_thickness, predators, 20))

    # Setting the speed of the while-loop
    clock = pygame.time.Clock() 

    ## Game loop
    run = True
    while run: 
        clock.tick(FPS)
        # Iterate over all game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            ## Event handling for the toggle buttons
            # Get the mouse position
            pos = pygame.mouse.get_pos()  
            # Checks if button has been clicked
            if separation_button.check_clicked(event, pos):
                # If button has been clicked change boolen for separation_on
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

        ## Move the predators
        for predator in predators:
            predator.update(WIDTH, HEIGHT)

        ## Draw the background and border
        WIN.blit(SPACE, (0,0))
        WIN.blit(border,(0,0))
        WIN.blit(border,(0,HEIGHT-border_thickness))

        ## Draw boids
        for boid in boids:
            boid.draw(WIN)

        ## Draw predators
        count = 0
        for predator in predators:
            predator.draw(WIN)
            count += predator.count
        
        font = pygame.font.SysFont('calibri',27)
        killed = font.render("Killed boids: " +str(count), True, (115, 170,200))
        WIN.blit(killed, (10,40))
        
        ## Draw toggle buttons
        alignment_button.draw()
        separation_button.draw()
        cohesion_button.draw()

        #Update game display
        pygame.display.update()


    ## Quit Pygame and exit
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()