import pygame
import sys
from pygame.locals import *

# Constants for the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LIGHT_BLUE = (100, 149, 237)
GREEN = (0, 255, 0)

# Player settings
PLAYER_RADIUS = 10
PLAYER_SPEED = 5

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PLAYER_RADIUS

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Insanity Run")

    clock = pygame.time.Clock()

    player = Player(50, SCREEN_HEIGHT // 2)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[K_LEFT]:
            dx = -PLAYER_SPEED
        if keys[K_RIGHT]:
            dx = PLAYER_SPEED
        if keys[K_UP]:
            dy = -PLAYER_SPEED
        if keys[K_DOWN]:
            dy = PLAYER_SPEED

        # Move the player
        player.move(dx, dy)

        # Draw the player
        screen.fill(LIGHT_BLUE)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
