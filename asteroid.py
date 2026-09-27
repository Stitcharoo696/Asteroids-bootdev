import random

import circleshape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
import pygame

from logger import log_event

class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            give_me_an_angle = random.uniform(20, 50)
            velocityA = self.velocity.rotate(give_me_an_angle)
            velocityB = self.velocity.rotate(give_me_an_angle * -1)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroidA = Asteroid(self.position.x, self.position.y, new_radius)
            asteroidA.velocity = velocityA * 1.2
            asteroidB = Asteroid(self.position.x, self.position.y, new_radius)
            asteroidB.velocity = velocityB * 1.2