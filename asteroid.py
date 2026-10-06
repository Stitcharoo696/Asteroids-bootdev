import random

from rock import Rock
import circleshape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH, TINY_COLORS, PLAYER_SHOOT_SPEED
import pygame

from logger import log_event

def random_tiny_color():
        return random.choice(TINY_COLORS)

class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float, color: str) -> None:
        super().__init__(x, y, radius)
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

  

    def split(self):
        if self.color == "red":
             rock_COUNT = random.randint(1, 5)
             for each_rock in range(rock_COUNT):
                angle = random.uniform(0, 360)
                direction = pygame.Vector2(1, 0).rotate(angle)
                speed = PLAYER_SHOOT_SPEED + random.uniform(5, 25)
                velocity = direction * speed
                a_rock = Rock(self.position.x, self.position.y)
                a_rock.velocity = velocity

        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            give_me_an_angle = random.uniform(20, 50)
            velocityA = self.velocity.rotate(give_me_an_angle)
            velocityB = self.velocity.rotate(give_me_an_angle * -1)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            if new_radius <= ASTEROID_MIN_RADIUS:
                new_colorA = random_tiny_color()
                new_colorB = random_tiny_color()
            else:
                new_colorA = "white"
                new_colorB = "white"
            asteroidA = Asteroid(self.position.x, self.position.y, new_radius, new_colorA)
            asteroidA.velocity = velocityA * 1.2
            asteroidB = Asteroid(self.position.x, self.position.y, new_radius, new_colorB)
            asteroidB.velocity = velocityB * 1.2


    def is_tiny(self) -> bool:
        return self.radius <= ASTEROID_MIN_RADIUS


    