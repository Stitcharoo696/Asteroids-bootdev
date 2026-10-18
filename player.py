from circleshape import CircleShape
import pygame
from constants import LINE_WIDTH, PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0

    # player is visually a triangle, so this method calculates the three points of the triangle based on the player's position, rotation, and radius. The triangle is drawn with the draw method, which uses pygame's polygon drawing function to render the triangle on the screen.
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    #draw the triangle sprite on the screen using pygame's polygon drawing function, which takes a list of points and draws a filled polygon with the specified color and line width
    def draw(self, screen):
        triangle = self.triangle()
        pygame.draw.polygon(screen, "white", triangle, LINE_WIDTH)

    #show and update the player's position, rotation, and shot cooldown based on user input. The player can rotate left or right using the A and D keys, move forward or backward using the W and S keys, and shoot using the spacebar. The shot cooldown prevents the player from shooting too quickly.
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    #input from keyboard controlls the player ship, which can rotate, move, and shoot based on the keys pressed. The player's position is updated based on the forward direction and speed, and the shot cooldown is decremented over time to allow for shooting at a controlled rate.
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown > 0:
                pass
            else:
                self.shoot()
                self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        self.shot_cooldown -= dt 

    #movement speed
    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    #shooting method for the player ship, which creates a new Shot object at the player's position and sets its velocity based on the player's rotation and the defined PLAYER_SHOOT_SPEED constant. The shot is added to the appropriate sprite group for rendering and collision detection.
    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED