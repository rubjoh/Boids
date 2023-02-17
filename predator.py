from objects import Object
from pygame.math import Vector2
import random

class Predator(Object):
    def __init__(self, x, y, image, screen_width, screen_height, boids, borders, predators, max_kill):
        super().__init__(x, y, image, screen_width, screen_height)
        self.boids = boids
        self.borders = borders
        self.predators = predators
        self.count = 0 
        self.max_kill = max_kill
        self.neighborhood = 75

    def cohesion(self):
        '''Method that moves the predators to the mean of the boids in it's neighborhood'''
        ## Calculate mean position of a flock
        count = 0
        mean_pos = Vector2(0, 0)
        for boid in self.boids:
            # Check if the boid is in the predators neighborhood
            if (boid.position - self.position).length() < self.neighborhood:
                mean_pos += boid.position
                count += 1
        if count > 0:
            mean_pos /= count

        # Calculate the vector towards the mean position and nomalize it 
        towards_mean = (mean_pos - self.position).normalize()

        # Adjust the velocity vector towards the mean position
        # Weight controls the strength of the cohesion behavior
        weight = 0.06
        self.velocity += towards_mean * weight
    
    def alignment(self):
        '''Method that moves the boid towards steer the boid so that it's velocity 
        vector is in the same direction as the other boids.'''

        ## Calculate the mean velocity of the local flocks
        n_boids = 0
        mean_velocity = Vector2(0, 0)
        for boid in self.boids:
            if (boid.position - self.position).length() < self.neighborhood:
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
            weight = 0.04
            self.velocity += towards_mean * weight

    def separation(self):
        '''Method that avoids collision with other predators'''
        steering = Vector2(0, 0)
        for predator in self.predators:
            if predator is not self and (predator.position - self.position).length() < 40:
                diff_vec = self.position - predator.position
                diff_length = diff_vec.length()
                if diff_length > 0:
                    # Weight the steering force based on the distance to the other boid
                    steering += diff_vec.normalize() / diff_length
        if steering.length() > 0:
            # Normalize the steering force and apply a weight to control its strength
            steering = steering.normalize() 
            self.velocity += steering * 0.05
    
    def eliminate(self):
        '''Method for eliminating boids'''
        ## Iterate over all boids
        for boid in self.boids:
            # Check distance between predator and boid, pluss max eliminate limit
            if (boid.position - self.position).length() < 10 and self.count < self.max_kill:
                # Remove boid
                self.boids.remove(boid)
                # Update the kill count
                self.count +=1

    def update(self, width, height):

        # Update the position based on velocity
        self.position += self.velocity

        ## Check if predator is out of the screen and flip the position to opposite side
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

        # Calling method for aligning the velocity vectors with the boids velocity vector
        self.alignment()

        # Calling method for cohesion behavior towards boids
        self.cohesion()
        
        # Calling elimination method
        self.eliminate()

        # Limit the speed of the boid
        max_speed = 1.2
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

        # Limit the acceleration of the boid
        max_acceleration = 0.4
        if self.velocity.length() > 0:
            acceleration = self.velocity.normalize() * max_acceleration
            self.velocity += acceleration
            if self.velocity.length() > max_speed:
                self.velocity.scale_to_length(max_speed)