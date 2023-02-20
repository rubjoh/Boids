import pygame
import pygame_gui
import os 
import random
from boids import Boids
from button import ToggleButton
from predator import Predator
from obstacle import Obstacle

## Defining some constants 
FPS = 120
WIDTH, HEIGHT = 1200, 900
DEFAULT_N_BOIDS = 35
MAX_OBSTACLES = 15
MAX_BOIDS = 70
MAX_PREDATORS = 15

# Initialize Pygame
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids")

## Load images
boid = pygame.image.load(os.path.join("Assets", "test.png"))
SPACE1 = pygame.image.load(os.path.join("Assets", "the11.jpg"))
predator = pygame.image.load(os.path.join("Assets", "ufo.png"))
obstacle = pygame.image.load(os.path.join("Assets", "planet2.png"))
obstacle_2 = pygame.image.load(os.path.join("Assets", "planet1.png"))
obstacle_3 = pygame.image.load(os.path.join("Assets", "planet3.png"))
obstacle_4 = pygame.image.load(os.path.join("Assets", "planet4.png"))
obstacle_5 = pygame.image.load(os.path.join("Assets", "planet5.png"))
obstacle_6 = pygame.image.load(os.path.join("Assets", "planet6.png"))

## Resize images 
boid_WIDTH, boid_HEIGHT = int(boid.get_width() * 0.08), int(boid.get_height() * 0.08)
boid1 = pygame.transform.scale(boid, (boid_WIDTH, boid_HEIGHT))
predator1 = pygame.transform.scale(predator, (100, 100))
SPACE = pygame.transform.scale(SPACE1, (WIDTH, HEIGHT))
obstacle1 = pygame.transform.scale(obstacle, (100, 100))
obstacle2 = pygame.transform.scale(obstacle_2, (100, 100))
obstacle3 = pygame.transform.scale(obstacle_3, (150, 150))
obstacle4 = pygame.transform.scale(obstacle_4, (120, 120))
obstacle5 = pygame.transform.scale(obstacle_5, (150, 150))
obstacle6 = pygame.transform.scale(obstacle_6, (120, 150))


## Creating a list with different obstacles
obs = [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6]

## Create the borders
border_thickness = 25
border = pygame.Surface((WIDTH, border_thickness))
border.fill((100,150,110))

## Define simple toggle buttons
separation_button = ToggleButton(
    x=WIDTH - 180,
    y=40,
    width=200,
    height=50,
    on_text="Separation: On",
    off_text="Separation: Off",
    font=pygame.font.SysFont("calibri",22),
    on_color=(0, 255, 0),
    off_color=(255, 0, 0),
    screen=WIN,
    initial_state=True
)

cohesion_button = ToggleButton(
    x=WIDTH - 180,
    y=90,
    width=200,
    height=50,
    on_text="Cohesion: On",
    off_text="Cohesion: Off",
    font=pygame.font.SysFont("calibri",22),
    on_color=(0, 255, 0),
    off_color=(255, 0, 0),
    screen=WIN,
    initial_state=True
)

alignment_button = ToggleButton(
    x=WIDTH - 180,
    y=140,
    width=200,
    height=50,
    on_text="Alignment: On",
    off_text="Alignment: Off",
    font=pygame.font.SysFont("calibri",22),
    on_color=(0, 255, 0),
    off_color=(255, 0, 0),
    screen=WIN,
    initial_state=True
)

predator_button = ToggleButton(
    x=WIDTH - 380,
    y=750,
    width=100,
    height=30,
    on_text="Add Alien",
    off_text="Add Alien",
    font=pygame.font.SysFont("calibri",20),
    on_color=(0, 255, 0),
    off_color=(0, 255, 0),
    screen=WIN,
    initial_state=True
)

predator_button_off = ToggleButton(
    x=WIDTH - 210,
    y=750,
    width=100,
    height=30,
    on_text="Remove Alien",
    off_text="Remove Alien",
    font=pygame.font.SysFont("calibri",20),
    on_color=(255, 0, 0),
    off_color=(255, 0, 0),
    screen=WIN,
    initial_state=True
)

boid_button = ToggleButton(
    x=WIDTH - 380,
    y=790,
    width=150,
    height=30,
    on_text="Add Spacepeople",
    off_text="Add Spacepeople",
    font=pygame.font.SysFont("calibri",20),
    on_color=(0, 255, 0),
    off_color=(0, 255, 0),
    screen=WIN,
    initial_state=True
)

boid_button_off = ToggleButton(
    x=WIDTH - 210,
    y=790,
    width=150,
    height=30,
    on_text="Remove Spacepeople",
    off_text="Remove Spacepeople",
    font=pygame.font.SysFont("calibri",20),
    on_color=(255, 0, 0),
    off_color=(255, 0, 0),
    screen=WIN,
    initial_state=True
)

obstacle_button = ToggleButton(
    x=WIDTH - 380,
    y=830,
    width=100,
    height=30,
    on_text="Add Obstacle",
    off_text="Add Obstacle",
    font=pygame.font.SysFont("calibri",20),
    on_color=(0, 255, 0),
    off_color=(0, 255, 0),
    screen=WIN,
    initial_state=True
)

obstacle_button_off = ToggleButton(
    x=WIDTH - 210,
    y=830,
    width=100,
    height=30,
    on_text="Remove Obstacle",
    off_text="Remove Obstacle",
    font=pygame.font.SysFont("calibri",20),
    on_color=(255, 0, 0),
    off_color=(255, 0, 0),
    screen=WIN,
    initial_state=True
)

def main():
    ## Create obstacles
    obstacles = []

    ## Create boids
    boids = []
    for i in range(DEFAULT_N_BOIDS):
        x = random.randint(50,WIDTH-50)
        y = random.randint(20,HEIGHT-20)
        boids.append(Boids(x, y, boid1, WIDTH, HEIGHT, boids, border_thickness, True, True, True, obstacles))

    ## Create predators
    predators = []

    # Setting the speed of the while-loop
    clock = pygame.time.Clock() 

    ## Game loop
    run = True
    while run: 
        clock.tick(FPS)

        ## Draw the background and border
        WIN.blit(SPACE, (0,0))
        WIN.blit(border,(0,0))
        WIN.blit(border,(0,HEIGHT-border_thickness))

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

            if predator_button.check_clicked(event, pos):
                # Check if maximum number of predators has been reached
                if len(predators) == MAX_PREDATORS:
                    ## Display error message
                    error_font = pygame.font.SysFont("calibri",50)
                    error = error_font.render("You've reached the maxiumum limit of aliens ", True, (250, 0,0))
                    WIN.blit(error, (WIDTH//2 - 520,HEIGHT//2 - 70))
                    # Update display so that text gets displyed on screen
                    pygame.display.update()
                    # Pause game for 21ms so that user have time to observe message
                    pygame.time.delay(2100)
                else:
                    # If the limit has not been reach, then add predators
                    predator = Predator(random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30), 
                                    predator1, WIDTH, HEIGHT, boids, border_thickness, predators, 20, obstacles)
                    predators.append(predator)

            if predator_button_off.check_clicked(event, pos):
                # Check that list of predators is not empty
                if len(predators) > 0:
                    predators.pop()
                # If there are no predators, raise error message
                else:
                    ## Create font and error message to be displayed
                    error_font = pygame.font.SysFont("calibri",50)
                    error = error_font.render("There are no aliens to remove! ", True, (250, 0,0))
                    WIN.blit(error, (WIDTH//2 - 400,HEIGHT//2 - 70))
                    # Update display so that text gets displyed on screen
                    pygame.display.update()
                    # Pause game for 19ms so that user have time to observe message
                    pygame.time.delay(1900)

            if boid_button.check_clicked(event, pos):
                # Check if maximum number of boids has been reached
                if len(boids) == MAX_BOIDS:
                    ## Display error message
                    error_font = pygame.font.SysFont("calibri",50)
                    error = error_font.render("You've reached the maxiumum limit of spacepeople ", True, (250, 0,0))
                    WIN.blit(error, (WIDTH//2 - 580,HEIGHT//2 - 70))
                    # Update display so that text gets displyed on screen
                    pygame.display.update()
                    # Pause game for 19ms so that user have time to observe message
                    pygame.time.delay(1900)
                else:
                    # If the limit has not been reached, then add boids
                    boid = Boids(random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30), boid1, WIDTH, HEIGHT, 
                                boids, border_thickness, True, True, True, obstacles)
                    boids.append(boid)

            if boid_button_off.check_clicked(event, pos):
                # Check that list of boids is not empty
                if len(boids) > 0:
                    boids.pop()
                # If there are no boids, error message will be raised 
                else:
                    error_font = pygame.font.SysFont("calibri",50)
                    error = error_font.render("There are no spacepeople to remove! ", True, (250, 0,0))
                    WIN.blit(error, (WIDTH//2 - 420,HEIGHT//2 - 70))
                    # Update display so that text gets displyed on screen
                    pygame.display.update()
                    # Pause game for 19ms so that user have time to observe message
                    pygame.time.delay(1900)
            
            if obstacle_button.check_clicked(event, pos):
                ## Check if conditions for creating obstacles is met
                while True:
                    # Check if maximum number of obstacles has been reached
                    if len(obstacles) == MAX_OBSTACLES:
                        ## Display error message
                        error_font = pygame.font.SysFont("calibri",50)
                        error = error_font.render("You've reached the maxiumum limit of obstacles ", True, (250, 0,0))
                        WIN.blit(error, (WIDTH//2 - 540,HEIGHT//2 - 70))
                        # Update display so that text gets displyed on screen
                        pygame.display.update()
                        # Pause game for 19ms so that user have time to observe message
                        pygame.time.delay(1900)
                        break
                    
                    ## Only append obstacle if distance to other obstacles is sufficient
                    obstacle = Obstacle(random.randint(40, WIDTH-40), random.randint(150, HEIGHT-150), random.choice(obs), WIDTH, HEIGHT)
                    # Check distance between current obstacle and all the others
                    if all((ob.position - obstacle.position).length() > 200 for ob in obstacles):
                        # Append obstacle if distance criteria is met
                        obstacles.append(obstacle)
                        break

            if obstacle_button_off.check_clicked(event, pos):
                # Check that list of obstacles is not empty
                if len(obstacles) > 0:
                    obstacles.pop()
                # If there are no obstacles, error message will be raised 
                else:
                    error_font = pygame.font.SysFont("calibri",50)
                    error = error_font.render("There are no obstacles to remove! ", True, (250, 0,0))
                    WIN.blit(error, (WIDTH//2 - 420,HEIGHT//2 - 70))
                    # Update display so that text gets displyed on screen
                    pygame.display.update()
                    # Pause game for 21ms so that user have time to observe message
                    pygame.time.delay(2100)
    
        ## Move the boids
        for boid in boids:
            boid.update(WIDTH, HEIGHT)

        ## Move the predators
        for predator in predators:
            predator.update(WIDTH, HEIGHT)

        ## Draw boids
        for boid in boids:
            boid.draw(WIN)

        ## Draw predators
        count = 0
        test = []
        for predator in predators:
            predator.draw(WIN)
            count += predator.count
            test.append(predator.killed)

        if len(test) == 0:
            test.append(0)

        ## Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(WIN)
        
        ## Display number of lost spacepeople
        font = pygame.font.SysFont("calibri",20)
        killed = font.render("Lost Spacepeople: " +str(test[0]), True, (67, 176,230))
        WIN.blit(killed, (10,80))

        ## Display number of predators, boids and obstacles
        n_boids = font.render("Alive Spacepeople: " +str(len(boids)) + str("/") + str(MAX_BOIDS), True, (67, 176,230))
        n_predators = font.render("Number Of Aliens : " +str(len(predators)) + str("/") + str(MAX_PREDATORS), True, (67, 176,230))
        n_obstacles = font.render("Number Of Planets : " +str(len(obstacles)) + str("/") + str(MAX_OBSTACLES), True, (67, 176,230))
        WIN.blit(n_boids, (10,40))
        WIN.blit(n_predators, (10,120))
        WIN.blit(n_obstacles, (10,160))

        
        ## Draw toggle buttons
        alignment_button.draw()
        separation_button.draw()
        cohesion_button.draw()
        predator_button.draw()
        predator_button_off.draw()
        boid_button.draw()
        boid_button_off.draw()
        obstacle_button.draw()
        obstacle_button_off.draw()

        #Update game display
        pygame.display.update()


    ## Quit Pygame and exit
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()