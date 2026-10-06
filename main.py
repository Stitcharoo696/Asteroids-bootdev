import sys

import pygame
from asteroid import Asteroid
import asteroidfield
from constants import START_SCORE
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from shot import Shot
from rock import Rock

def main():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    rocks = pygame.sprite.Group()

    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    asteroid_field = asteroidfield.AsteroidField()
    Rock.containers = (updatable, drawable)

    score = START_SCORE

    pygame.init()
    pygame.font.init()

    score_font = pygame.font.Font(None, 36)

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

    def points_for_asteroid(color):
        if color == "yellow":
            return 100
        if color == "blue":
            return 200
        if color == "red":
            return 500
        return 0

    #print(points_for_asteroid("yellow"))  # 100
    #print(points_for_asteroid("blue"))    # 200
    #print(points_for_asteroid("red"))     # 500

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
                print(f"Final score: {score}")
                sys.exit()

        for object in asteroids:
            for shot in shots:
                if shot.collides_with(object):
                    log_event("asteroid_shot")
                    was_tiny = object.is_tiny()
                    asteroid_color = object.color
                    object.split()
                    if was_tiny:
                        score += points_for_asteroid(object.color)
                    shot.kill()
        for sprite in drawable:
            sprite.draw(screen)

        score_text = score_font.render(f"Score: {score}", True, "white")
        score_rect = score_text.get_rect()
        score_rect.midtop = (SCREEN_WIDTH / 2, 10)
        screen.blit(score_text, score_rect)
        pygame.display.flip()
        
        #print(f"{dt}")


if __name__ == "__main__":
    main()
