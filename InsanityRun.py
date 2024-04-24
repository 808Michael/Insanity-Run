import pygame
import sys
from pygame.locals import *

# Constants for the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LIGHT_BLUE = (173, 216, 250)
BLUE = (100, 149, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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


class Level1:
    def __init__(self):
        self.top_line = [(100, 100), (700, 100)]
        self.bottom_line = [(100, 500), (700, 500)]
        self.square_left = [(50, 250), (100, 250), (100, 350), (50, 350)]
        self.square_right = [(750, 250), (700, 250), (700, 350), (750, 350)]

    def draw(self, screen):
        pygame.draw.line(screen, BLACK, self.top_line[0], self.top_line[1], 8)
        pygame.draw.line(screen, BLACK, self.bottom_line[0], self.bottom_line[1], 8)
        pygame.draw.line(screen, BLACK, self.square_left[0], self.square_left[1], 8)
        pygame.draw.line(screen, BLACK, self.square_left[2], self.square_left[3], 8)
        pygame.draw.line(screen, BLACK, self.square_left[3], self.square_left[0], 8)
        pygame.draw.line(screen, BLACK, self.square_right[0], self.square_right[1], 8)
        pygame.draw.line(screen, BLACK, self.square_right[2], self.square_right[3], 8)
        pygame.draw.line(screen, BLACK, self.square_right[3], self.square_right[0], 8)
        pygame.draw.line(screen, BLACK, (100, 100), (100, 250), 8)
        pygame.draw.line(screen, BLACK, (100, 500), (100, 350), 8)
        pygame.draw.line(screen, BLACK, (700, 100), (700, 250), 8)
        pygame.draw.line(screen, BLACK, (700, 500), (700, 350), 8)
        pygame.draw.polygon(screen, WHITE, [
            self.top_line[0], self.top_line[1],
            self.bottom_line[1], self.bottom_line[0],
        ], 0)
        pygame.draw.polygon(screen, BLUE, self.square_left, 0)
        pygame.draw.polygon(screen, BLUE, self.square_right, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Insanity Run")

    clock = pygame.time.Clock()

    level1 = Level1()
    player = Player(75, 300)

    pygame.mixer.init()

    pygame.mixer.music.load('mp3/535331_Stay-Inside-Me.mp3')

    pygame.mixer.music.play(loops=-1)

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

        player.move(dx, dy)

        screen.fill(LIGHT_BLUE)

        level1.draw(screen)

        player.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
