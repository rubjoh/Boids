import pygame
import os
import random
from pygame.math import Vector2

class Boids:
    def __init__(self, x, y, image, w, h, boids, borders):
        self.position = Vector2(x, y) 
        self.velocity = Vector2(random.randint(-2,2),random.randint(-2,2))
        self.image = image
        self.w = w
        self.h = h
        self.boids = boids
        self.neighborhood = 90
        self.borders = borders

    def draw(self, surface):
        '''Method that draws the boid as a triangle on the given surface. '''

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

    def update(self, width, height):

        # Save current position
        #current_pos = self.position.copy()

        # Update the position based on velocity
        self.position += self.velocity

        # Update the velocity 
        #self.velocity = self.position - current_pos

        ## Check if boid is out of the screen and flip the position to opposite side
        # Check left border
        if self.position.x < 0:
            self.position.x = width
        # Check right border
        elif self.position.x > width:
            self.position.x = 0
            
        # Check top and bottom borders
        self.position.y = max(self.position.y, self.borders + 30)
        self.position.y = min(self.position.y, height - self.borders - 30)
        if self.position.y == self.borders + 30 or self.position.y == height - self.borders - 30:
            self.velocity.y = -self.velocity.y


        # Calling method for anti-collision behavior
        self.separation()

        # Calling method for aligning the velocity vectors 
        self.alignment()

        # Calling method for cohesion behavior 
        self.cohesion()

        # Limit the speed of the boid
        max_speed = 1
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

        # Limit the acceleration of the boid
        max_acceleration = 0.3
        if self.velocity.length() > 0:
            acceleration = self.velocity.normalize() * max_acceleration
            self.velocity += acceleration
            if self.velocity.length() > max_speed:
                self.velocity.scale_to_length(max_speed)


    def cohesion(self):
        '''Method that calculates the mean position of boids and changes the velocity 
        vector towards the mean position of the flock.'''

        ## Calculate the mean position of the local flocks 
        n_boids = 0
        mean_pos = Vector2(0, 0)
        for boid in self.boids:
            if boid is not self and (boid.position - self.position).length() < self.neighborhood:
                mean_pos += boid.position
                n_boids += 1
        if n_boids > 0:
            mean_pos /= n_boids

        # Calculate the vector towards the mean position and nomalize it 
        # to ensure that speed in not increasing
        towards_mean = (mean_pos - self.position).normalize()

        # Adjust the velocity vector towards the mean position
        # Weight controls the strength of the cohesion behavior
        weight = 0.065
        self.velocity += towards_mean * weight


    def alignment(self):
        '''Method that moves the boid towards steer the boid so that it's velocity 
        vector is in the same direction as the other boids.'''

        ## Calculate the mean velocity of the local flocks
        n_boids = 0
        mean_velocity = Vector2(0, 0)
        for boid in self.boids:
            if boid is not self and (boid.position - self.position).length() < self.neighborhood:
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
            weight = 0.065
            self.velocity += towards_mean * weight


    def separation(self):
        '''Method that avoids collision with other boids'''
        steering = Vector2(0, 0)
        for boid in self.boids:
            if boid is not self and (boid.position - self.position).length() < 30:
                diff_vec = self.position - boid.position
                diff_length = diff_vec.length()
                if diff_length > 0:
                    # Weight the steering force based on the distance to the other boid
                    steering += diff_vec.normalize() / diff_length
        if steering.length() > 0:
            # Normalize the steering force and apply a weight to control its strength
            steering = steering.normalize() 
            self.velocity += steering * 0.07
 

