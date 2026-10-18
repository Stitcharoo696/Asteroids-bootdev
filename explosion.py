import pygame
from circleshape import CircleShape
from constants import EXPLOSION_RADIUS

# Explosion class for the game, which inherits from the CircleShape class in circleshape.py. It represents an explosion that occurs when an asteroid is destroyed. The explosion has a fixed radius and a limited lifetime, after which it is removed from the game.
class Explosion(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, EXPLOSION_RADIUS)
        self.lifetime = 0.5  # seconds
        self.elapsed_time = 0.0
    #defines the visual lifespan of the explosion sprite
    def update(self, dt: float) -> None:
        self.elapsed_time += dt
        if self.elapsed_time >= self.lifetime:
            self.kill()
    #draw override for explosion sprite, which draws a blue circle on the screen at the explosion's position with the defined radius
    def draw(self, screen):
       pygame.draw.circle(screen, "blue", self.position, self.radius,)