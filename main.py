import pygame
from logger import log_state

def main():
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


    while inf_loop != True:
        log_state()
        for event in pygame.event.get():
            pass
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        #print(f"{dt}")


if __name__ == "__main__":
    main()
