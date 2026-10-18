import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH

#rocks fired from red asteroids that can hit the player ship and end the game. The Rock class inherits from the CircleShape class in circleshape.py and has a fixed radius and color. The rock's position is updated based on its velocity, which is set when it is created by the Asteroid class.
class Rock(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    #draw the rock sprite on the screen using pygame's circle drawing function, which takes the position, radius, color, and line width as parameters
    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "red",
            self.position,
            self.radius,
            LINE_WIDTH,
        )
    #update the rock's position based on its velocity and the time delta, which is passed in as a parameter. The rock's position is updated by adding the product of its velocity and the time delta to its current position
    def update(self, dt):
        self.position += self.velocity * dt