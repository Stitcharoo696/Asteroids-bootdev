import sys

import pygame
from asteroid import Asteroid
import asteroidfield
from constants import EXPLOSION_RADIUS, START_SCORE
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from shot import Shot
from rock import Rock
from explosion import Explosion

def main():
    #groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    rocks = pygame.sprite.Group()

    #containers
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    asteroid_field = asteroidfield.AsteroidField()
    Rock.containers = (updatable, drawable)
    Explosion.containers = (updatable, drawable)
    
    #reset score to 0 at start of game
    score = START_SCORE


    #initialize game and font
    pygame.init()
    pygame.font.init()
    #set score font to default pygame font with size 36
    score_font = pygame.font.Font(None, 36)
    #start tracking time and time difference between frames
    clock = pygame.time.Clock()
    dt = 0.0
    #log pygame version and screen dimensions
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    from constants import SCREEN_WIDTH
    from constants import SCREEN_HEIGHT
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #update game loop controller variable to allow for game loop to run until user quits
    inf_loop = False

    #containers out of phase with class definitions, so we need to set them here after the classes have been defined
    Rock.containers = (rocks, updatable, drawable)
    Player.containers = (updatable, drawable)

    #place the player ship in the center of the screen at the start of the game
    player_ship = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    #another out of phase container assignment, this time for the Asteroid class - see wikipedia "load bearing coconut"
    Asteroid.containers = (asteroids, updatable, drawable)

    #setting the score counts for each scoring action in the game, based on the color of the asteroid destroyed
    def points_for_asteroid(color):
        if color == "yellow":
            return 50
        if color == "blue":
            return 100
        if color == "red":
            return 500
        if color == "white":
            return 25
        return 0

    #debugging code to test the points_for_asteroid function
    #print(points_for_asteroid("yellow"))  
    #print(points_for_asteroid("blue"))    
    #print(points_for_asteroid("red"))     

    #game update loop - this is where the game runs until the user quits or dies
    while inf_loop != True:
        
        log_state()
        #quit statement to allow the user to quit the game by closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #delta of time between frames, used to update the game state and draw the game at a consistent speed regardless of the frame rate
        dt = clock.tick(60) / 1000
        #draw the screen every frame, fill the screen with black, update the game state, check for collisions between the player ship and asteroids or rocks, check for collisions between shots and asteroids, draw all drawable objects, and update the score display
        screen.fill("black")
        updatable.update(dt)

        #check for collisions between the player ship and asteroids or rocks, and end the game if a collision occurs and print final score to the console
        for asteroid in asteroids:
            if player_ship.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                print(f"Final score: {score}")
                sys.exit()

        #check for collisions between the player ship and rocks from red asteroids, and end the game if a collision occurs and print final score to the console
        for rock in rocks:
            if player_ship.collides_with(rock):
                log_event("player_hit")
                print("Game over!")
                print(f"Final score: {score}")
                sys.exit()

        #check size and color of asteroids.
        #if big asteroid is shot, split it into two smaller asteroids
        #if tiny asteroid is shot, destroy it and add points to the score based on the color of the asteroid
        #if a blue asteroid is shot, create an explosion that destroys all asteroids and the player ship within the explosion radius, and add points to the score based on the number of objects destroyed in the explosion
        #run red tiny asteroid from asteroid class, which creates rocks that can hit the player ship and end the game
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    was_tiny = asteroid.is_tiny()
                    asteroid_color = asteroid.color
                    was_blue = asteroid_color == "blue"
                    explosion_position = asteroid.position.copy()


                    asteroid.split()
                    #score points for destroying a tiny asteroid, based on the color of the asteroid
                    if was_tiny:
                        score += points_for_asteroid(asteroid_color)
                    if was_tiny and was_blue:
                        
                        #place holder variable for how many objects destroyed in a single blue asteroid explosion
                        destroyed_count = 0
                        log_event("blue_asteroid_explosion")
                        Explosion(explosion_position.x, explosion_position.y)
                        player_was_hit = (player_ship.position.distance_to(explosion_position) <= EXPLOSION_RADIUS)

                        #count how many objects destroyed and remove them from the game, and add to the score based on the number of objects destroyed
                        for target in asteroids.copy():
                            distance = target.position.distance_to(explosion_position)
                            if distance <= EXPLOSION_RADIUS:
                                target.kill()
                                destroyed_count += 1

                        if player_was_hit:
                            destroyed_count += 1 
                             
                        #calculate score for all objects hit by the blue asteroid explosion, with a bonus multiplier for each additional object destroyed in the same explosion
                        base_points = 100 * destroyed_count
                        bonus_multiplier = 1 + (destroyed_count * 0.05)
                        total = int(base_points * bonus_multiplier)
                        score += total

                        #end game if player is caught in explosion
                        if player_was_hit:

                            log_event("player_hit")
                            print("You were hit by the explosion!")  
                            print("Game over!")
                            print(f"Final score: {score}")
                            sys.exit()



                    shot.kill()
        for sprite in drawable:
            sprite.draw(screen)
        #display the score at the top of the screen, centered horizontally
        score_text = score_font.render(f"Score: {score}", True, "white")
        score_rect = score_text.get_rect()
        score_rect.midtop = (SCREEN_WIDTH / 2, 10)
        screen.blit(score_text, score_rect)
        pygame.display.flip()
        
        #print(f"{dt}")


if __name__ == "__main__":
    main()