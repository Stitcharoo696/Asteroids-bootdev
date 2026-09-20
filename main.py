import sys

import pygame
from asteroid import Asteroid
import asteroidfield
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField

def main():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    AsteroidField.containers = (updatable,)

    asteroid_field = asteroidfield.AsteroidField()

    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    from constants import SCREEN_WIDTH
    from constants import SCREEN_HEIGHT
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    inf_loop = False

    Player.containers = (updatable, drawable)
    player_ship = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    Asteroid.containers = (asteroids, updatable, drawable)



    while inf_loop != True:
        
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        dt = clock.tick(60) / 1000
        screen.fill("black")
        updatable.update(dt)
        for object in asteroids:
            if player_ship.collides_with(object):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        for sprite in drawable:
            sprite.draw(screen)

       
        pygame.display.flip()
        
        #print(f"{dt}")


if __name__ == "__main__":
    main()
