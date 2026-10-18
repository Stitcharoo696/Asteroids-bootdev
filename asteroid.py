import random
from rock import Rock
import circleshape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH, TINY_COLORS, PLAYER_SHOOT_SPEED
import pygame
from logger import log_event

#choose a color from the constants.py TINY_COLORS list at random for the tiny asteroids that are created when a larger asteroid is destroyed
def random_tiny_color():
        return random.choice(TINY_COLORS)

#asteroid sprite creation, drawing, and updating class, which inherits from the CircleShape class in circleshape.py
class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float, color: str) -> None:
        super().__init__(x, y, radius)
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

  
    #split method for the Asteroid class, which is called when an asteroid is hit by a shot. If the asteroid is red, it will create a random number of rocks that can hit the player ship and end the game. If the asteroid is not red, it will split into two smaller asteroids if it is larger than the minimum radius, or be destroyed if it is already at the minimum radius. The new asteroids will have a random color if they are tiny, or be white if they are larger than the minimum radius.
    def split(self):
        if self.color == "red":
             rock_COUNT = random.randint(1, 5)
             for each_rock in range(rock_COUNT):
                angle = random.uniform(0, 360)
                direction = pygame.Vector2(1, 0).rotate(angle)
                speed = PLAYER_SHOOT_SPEED * random.uniform(0.25, 1.02)
                velocity = direction * speed
                a_rock = Rock(self.position.x, self.position.y)
                a_rock.velocity = velocity

        #delete self from the game, and if the asteroid is larger than the minimum radius, create two smaller asteroids with a random color if they are tiny, or white if they are larger than the minimum radius
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

    #check for tiny radius of the asteroid, which is used to determine if the asteroid should be destroyed or split into smaller asteroids when hit by a shot
    def is_tiny(self) -> bool:
        return self.radius <= ASTEROID_MIN_RADIUS


    