import pygame
import sys
import math
from pygame.locals import *

# Constants for the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LIGHT_BLUE = (173, 216, 250)
BLUE = (100, 149, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT_SIZE = 24

# Player settings
PLAYER_RADIUS = 10
PLAYER_SPEED = 5


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PLAYER_RADIUS
        self.coins = 0

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)

    def move(self, dx, dy, level_lines):
        new_x = self.x + dx
        new_y = self.y + dy

        for line in level_lines:
            if self._is_colliding_with_line((self.x, self.y), (new_x, new_y), line):
                return

        self.x = new_x
        self.y = new_y

    def _is_colliding_with_line(self, start, end, line):
        x1, y1 = start
        x2, y2 = end
        x3, y3 = line[0]
        x4, y4 = line[1]

        denominator = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))

        if denominator == 0:
            return False

        ua = (((x4 - x3) * (y1 - y3)) - ((y4 - y3) * (x1 - x3))) / denominator
        ub = (((x2 - x1) * (y1 - y3)) - ((y2 - y1) * (x1 - x3))) / denominator

        if 0 <= ua <= 1 and 0 <= ub <= 1:
            return True
        return False


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

    def get_line_rects(self):
        rects = []
        rects.append(pygame.Rect(self.top_line[0], (self.top_line[1][0] - self.top_line[0][0], 8)))
        rects.append(pygame.Rect(self.bottom_line[0], (self.bottom_line[1][0] - self.bottom_line[0][0], 8)))
        rects.append(pygame.Rect(self.square_left[0], (50, 100)))
        rects.append(pygame.Rect(self.square_right[1], (50, 100)))
        return rects


class RedSquare:
    def __init__(self, center, angle_offset, radius):
        self.center = center
        self.angle_offset = angle_offset
        self.radius = radius
        self.angle = 0
        self.x = center[0]
        self.y = center[1]

    def update_position(self):
        self.angle += 2
        self.angle %= 360
        self.x = self.center[0] + self.radius * math.cos(math.radians(self.angle + self.angle_offset))
        self.y = self.center[1] + self.radius * math.sin(math.radians(self.angle + self.angle_offset))

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x - 5, self.y - 5, 10, 10))


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

    death_sound = pygame.mixer.Sound("mp3/geometry-dash-death-sound-effect.mp3")

    attempts = 0
    current_level = 1
    total_levels = 5

    font = pygame.font.Font(None, FONT_SIZE)

    red_squares_150_150 = []
    for i in range(4):
        angle_offset = i * 90
        red_square = RedSquare((150, 150), angle_offset, 50)
        red_squares_150_150.append(red_square)

    red_squares_150_450 = []
    for i in range(4):
        angle_offset = i * 90
        red_square = RedSquare((150, 450), angle_offset, 50)
        red_squares_150_450.append(red_square)

    red_squares_650_150 = []
    for i in range(4):
        angle_offset = i * 90
        red_square = RedSquare((650, 150), angle_offset, 50)
        red_squares_650_150.append(red_square)

    red_squares_650_450 = []
    for i in range(4):
        angle_offset = i * 90
        red_square = RedSquare((650, 450), angle_offset, 50)
        red_squares_650_450.append(red_square)

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

        level_lines = [
            (level1.top_line[0], level1.top_line[1]),
            (level1.bottom_line[0], level1.bottom_line[1]),
            ((100, 100), (100, 250)),
            ((100, 500), (100, 350)),
            ((700, 100), (700, 250)),
            ((700, 500), (700, 350)),
            (level1.square_left[0], level1.square_left[1]),
            (level1.square_left[2], level1.square_left[3]),
            (level1.square_left[3], level1.square_left[0]),
            (level1.square_right[0], level1.square_right[1]),
            (level1.square_right[2], level1.square_right[3]),
            (level1.square_right[3], level1.square_right[0]),
        ]
        player.move(dx, dy, level_lines)

        for red_square_group in [red_squares_150_150, red_squares_150_450, red_squares_650_150, red_squares_650_450]:
            for red_square in red_square_group:
                distance = math.hypot(player.x - red_square.x, player.y - red_square.y)
                if distance < PLAYER_RADIUS + 5:
                    player.x = 75
                    player.y = 300

                    attempts += 1

                    death_sound.play()

        screen.fill(LIGHT_BLUE)

        level1.draw(screen)

        for red_square in red_squares_150_150:
            red_square.update_position()
            red_square.draw(screen)

        for red_square in red_squares_150_450:
            red_square.update_position()
            red_square.draw(screen)

        for red_square in red_squares_650_150:
            red_square.update_position()
            red_square.draw(screen)

        for red_square in red_squares_650_450:
            red_square.update_position()
            red_square.draw(screen)

        coin_size = 10
        coin_image = pygame.Surface((coin_size, coin_size), pygame.SRCALPHA)
        pygame.draw.circle(coin_image, (255, 215, 0), (coin_size // 2, coin_size // 2), coin_size // 2)
        coin_rect = coin_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(coin_image, coin_rect)

        coin_radius = 20
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                offset_x = i * coin_radius
                offset_y = j * coin_radius
                coin_rect = coin_image.get_rect(center=(SCREEN_WIDTH // 2 + offset_x, SCREEN_HEIGHT // 2 + offset_y))
                screen.blit(coin_image, coin_rect)

        coin_rect = coin_image.get_rect(center=(150, 150))
        screen.blit(coin_image, coin_rect)

        coin_rect = coin_image.get_rect(center=(650, 150))
        screen.blit(coin_image, coin_rect)

        coin_rect = coin_image.get_rect(center=(150, 450))
        screen.blit(coin_image, coin_rect)

        coin_rect = coin_image.get_rect(center=(650, 450))
        screen.blit(coin_image, coin_rect)

        player.draw(screen)

        attempts_text = font.render("Attempts: {}".format(attempts), True, BLACK)
        text_rect = attempts_text.get_rect(center=(SCREEN_WIDTH // 2, FONT_SIZE))
        screen.blit(attempts_text, text_rect)

        coins_text = font.render("Coins: {}".format(player.coins), True, BLACK)
        screen.blit(coins_text, (10, 10))

        level_text = font.render("Level {}/{}".format(current_level, total_levels), True, BLACK)
        level_rect = level_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(level_text, level_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
