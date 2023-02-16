import pygame
import os
import random
from pygame.math import Vector2

class Boids:
    def __init__(self, x, y, image, w, h, boids):
        self.position = Vector2(x, y) 
        self.velocity = Vector2(random.randint(-1,1),random.randint(-1,1))
        self.image = image
        self.w = w
        self.h = h
        self.boids = boids

    def draw(self, surface):
        '''Method that draws the boid as a triangle on the given surface.'''

        # Calculate the angle of rotation based on the direction of the velocity vector
        angle = -self.velocity.angle_to(Vector2(0, 0))

        # Rotate the image of the boid
        rotated_image = pygame.transform.rotate(self.image, angle)

        # Get the rectangle that encloses the rotated image
        rect = rotated_image.get_rect()

        # Set the center of the rectangle to the position of the boid
        rect.center = (int(self.position.x), int(self.position.y))

        # Draw the rotated image on the surface
        surface.blit(rotated_image, rect)


    def update(self, width, height):
        # Update the position based on velocity
        self.position += self.velocity

        ## Keep the boid within the screen
        # Check left border
        if self.position.x < 0:
            self.velocity.x = -self.velocity.x
            #self.image = pygame.transform.flip(self.image, True, False)

        # Check right border
        elif self.position.x > width-50:
            self.velocity.x = -self.velocity.x
            #self.image = pygame.transform.flip(self.image, True, False)

        # Check top border
        if self.position.y < 0:
            self.velocity.y = -self.velocity.y
            #self.image = pygame.transform.flip(self.image, False, True)

        # Check lower border
        elif self.position.y > height-50:
            self.velocity.y = -self.velocity.y
            #self.image = pygame.transform.flip(self.image, False, True)
        
        # Calling method for cohesion behavior 
        self.cohesion()

        # Calling method for anti-collision behavior
        self.separation()

        # Calling method for aligning the velocity vectors 
        self.alignment()

    def cohesion(self):
        '''Method that calculates the mean position of boids and changes the velocity 
        vector towards the mean position of the flock.'''

        ## Calculate the mean position of the local flocks 
        neighborhood = 10
        n_boids = 0
        mean_pos = Vector2(0, 0)
        for boid in self.boids:
            if boid is not self and (boid.position - self.position).length() < neighborhood:
                mean_pos += boid.position
                n_boids += 1
        if n_boids > 0:
            mean_pos /= n_boids

        # Calculate the vector towards the mean position and nomalize it 
        # to ensure that speed in not increasing
        towards_mean = (mean_pos - self.position).normalize()

        # Adjust the velocity vector towards the mean position
        # Weight controls the strength of the cohesion behavior
        weight = 0.01
        self.velocity += towards_mean * weight


    def alignment(self):
        '''Method that moves the boid towards steer the boid so that it's velocity 
        vector is in the same direction as the other boids.'''

        ## Calculate the mean velocity of the local flocks
        neighborhood = 10
        n_boids = 0
        mean_velocity = Vector2(0, 0)
        for boid in self.boids:
            if boid is not self and (boid.position - self.position).length() < neighborhood:
                mean_velocity += boid.velocity
                n_boids += 1
        if n_boids > 0:
            mean_velocity /= n_boids

        # If the mean velocity is not the zero vector, adjust the velocity vector
        if mean_velocity.length() > 0:
            # Calculate the direction of the mean velocity vector and nomalize it 
            # to ensure that speed is not increasing
            towards_mean = mean_velocity.normalize()

            # Adjust the velocity vector towards the mean velocity
            # Weight controls the strength of the alignment behavior
            weight = 0.01
            self.velocity += towards_mean * weight


    def separation1(self):
        '''Method that avoids collision with other boids'''
        for boid in self.boids:
            if boid is not self and (boid.position - self.position).length() < 10:
                self.velocity = -(boid.velocity).normalize()

    def separation(self):
        '''Method that avoids collision with other boids'''
        steering = Vector2(0, 0)
        neighborhood = 50
        for boid in self.boids:
            if boid is not self and (boid.position - self.position).length() < neighborhood:
                diff = self.position - boid.position
                diff_length = diff.length()
                if diff_length > 0:
                    # Weight the steering force based on the distance to the other boid
                    steering += diff.normalize() / diff_length
        if steering.length() > 0:
            # Normalize the steering force and apply a weight to control its strength
            steering = steering.normalize() * 0.1
            self.velocity += steering

