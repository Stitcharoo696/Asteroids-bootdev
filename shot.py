import circleshape
from constants import SHOT_RADIUS, LINE_WIDTH
import pygame

# Shot class for the game, which inherits from the CircleShape class in circleshape.py. It represents a shot fired by the player ship. The shot has a fixed radius and is drawn as a white circle on the screen. Its position is updated based on its velocity, which is set when it is created by the Player class.
class Shot(circleshape.CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
    
    #drw the player shots on the screen using pygame's circle drawing function, which takes the position, radius, color, and line width as parameters
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    #update the shot's position based on its velocity and the time delta, which is passed in as a parameter. The shot's position is updated by adding the product of its velocity and the time delta to its current position
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt