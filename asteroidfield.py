import random
from collections.abc import Callable
import pygame
from asteroid import Asteroid
from constants import *

#edge of the game screen, which is used to spawn asteroids at random positions along the edge of the screen
#I decided not to have it wrap around. But if I did wrap it, I would have a maximum limit on number of asteroids displayed at one time and a kill-timer on every asteroid, which would delete itself without giving points because the player was way too slow. Take that, player.
Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    edges: list[Edge] = [
        (
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ),
    ]
    #draw the sprites
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
    #spawn a new asteroid at a random edge of the screen, with a random speed and direction, and a random size based on the ASTEROID_KINDS constant
    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius, "white")
        asteroid.velocity = velocity
    #stagger spawning based on delta time
    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)