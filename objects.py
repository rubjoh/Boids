from pygame.math import Vector2
import pygame
import random

class Object:
    def __init__(self, x, y, image, screen_width, screen_height):
        self.pos = Vector2(x,y)
        self.velocity = Vector2(random.randint(-2,2),random.randint(-2,2))
        self.image = image
        self.w = screen_width
        self.h = screen_height
        

    def draw(self, surface):

        # Calculate the angle of rotation based on the direction of the velocity vector
        angle = self.velocity.angle_to(Vector2(0, -1))

        # Rotate the image of the boid
        rotated_image = pygame.transform.rotate(self.image, angle)

        # Get the rectangle that encloses the rotated image
        rect = rotated_image.get_rect()

        # Set the center of the rectangle to the position of the boid
        rect.center = (int(self.position.x), int(self.position.y))

        # Draw the rotated image on the surface
        surface.blit(rotated_image, rect)

    def move(self):
        pass

    def get_box(self):
        return self.image.get_rect(topleft=(self.x, self.y))
