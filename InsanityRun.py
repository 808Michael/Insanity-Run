import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Game")

# Set up the colors
LIGHT_BLUE = (173, 216, 230)
BLUE = (100, 149, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

# Global variables
circle_radius = 10
current_level = 2
coin_count = 0
attempts = 0

# Define font
font = pygame.font.SysFont("times new roman", 20)

# Music Module
pygame.mixer.init()

# Load the sound file
pygame.mixer.music.load('mp3/535331_Stay-Inside-Me.mp3')
death_sound = pygame.mixer.Sound('mp3/geometry-dash-death-sound-effect.mp3')

# Set the volume level
pygame.mixer.music.set_volume(0.5)

# Start playing sound on a loop
pygame.mixer.music.play(loops=-1)

# Function to handle key presses
def handle_key_presses(circle_x, circle_y, circle_speed, rect_x=None, rect_y=None, rect_width=None, rect_height=None):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and (rect_x is None or circle_x - circle_speed > rect_x):
        circle_x -= circle_speed
    if keys[pygame.K_RIGHT] and (rect_x is None or circle_x + circle_speed < rect_x + rect_width):
        circle_x += circle_speed
    if keys[pygame.K_UP] and (rect_y is None or circle_y - circle_speed > rect_y):
        circle_y -= circle_speed
    if keys[pygame.K_DOWN] and (rect_y is None or circle_y + circle_speed < rect_y + rect_height):
        circle_y += circle_speed
    return circle_x, circle_y


class OrbitingSquare:
    def __init__(self, center, angle_offset, radius, size):
        self.center = center
        self.angle_offset = angle_offset
        self.radius = radius
        self.size = size
        self.angle = 0
        self.x = center[0] + radius * math.cos(math.radians(angle_offset))
        self.y = center[1] + radius * math.sin(math.radians(angle_offset))
        self.last_update_time = pygame.time.get_ticks()

    def update_position(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_update_time
        self.last_update_time = current_time

        angle_increment = (elapsed_time / 1000) * 150

        self.angle += angle_increment
        self.angle %= 360
        self.x = self.center[0] + self.radius * math.cos(math.radians(self.angle + self.angle_offset))
        self.y = self.center[1] + self.radius * math.sin(math.radians(self.angle + self.angle_offset))

    def draw(self, screen):
        # Adjust size of the square based on self.size
        pygame.draw.rect(screen, RED, (self.x - self.size / 2, self.y - self.size / 2, self.size, self.size))


# Level 1
def level_1():
    global circle_x, circle_y, coins, circle_radius, current_level, coin_count, attempts
    attempts = 0

    # Set up square
    square_size = 500
    square_x = 150
    square_y = 50

    # Set up level 1 spawn
    circle_x = 175
    circle_y = 75
    circle_speed = 0.1

    # Set up gold coins
    coin_radius = 10
    coin_positions = [
        (300, 200),
        (400, 100),
        (600, 100),
        (200, 300),
        (400, 300),
        (600, 300),
        (200, 500),
        (400, 500),
        (500, 400),
        (625, 525),
    ]
    coins = coin_positions
    initial_coin_positions = coins[:]

    # List to store OrbitingSquare for each gold coin
    coin_orbiting_squares = []
    for coin_pos in coins[:-1]:
        coin_orbiting_squares.append(OrbitingSquare(center=coin_pos, angle_offset=0, radius=30, size=20))

    # Main loop
    while current_level == 1:
        # Clear window surface
        window.fill(LIGHT_BLUE)

        # Check if Shift key is being held down
        keys = pygame.key.get_pressed()
        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed, square_x, square_y, square_size,
                                                square_size)

        # Check for collision with gold coins
        for coin_pos in coins:
            coin_x, coin_y = coin_pos
            if (circle_x + circle_radius > coin_x - coin_radius and circle_x - circle_radius < coin_x + coin_radius
                    and circle_y + circle_radius > coin_y - coin_radius and circle_y - circle_radius < coin_y + coin_radius):
                coins.remove(coin_pos)
                coin_count += 1
                if len(coins) == 0:
                    current_level = 2
                break

        # Check for collision with player square
        for orbiting_square in coin_orbiting_squares:
            if (circle_x + circle_radius > orbiting_square.x - 5 and circle_x - circle_radius < orbiting_square.x + 5
                    and circle_y + circle_radius > orbiting_square.y - 5 and circle_y - circle_radius < orbiting_square.y + 5):

                if not shift_pressed:
                    death_sound.play()
                    attempts += 1

                    circle_x = 170
                    circle_y = 70

                    coins = initial_coin_positions[:]

        # Draw larger white square
        pygame.draw.rect(window, (255, 255, 255), (square_x, square_y, square_size, square_size))

        # Draw black lines on perimeter
        pygame.draw.line(window, BLACK, (square_x, square_y), (square_x + square_size, square_y), 3)
        pygame.draw.line(window, BLACK, (square_x, square_y), (square_x, square_y + square_size), 3)
        pygame.draw.line(window, BLACK, (square_x + square_size, square_y),
                         (square_x + square_size, square_y + square_size), 3)
        pygame.draw.line(window, BLACK, (square_x, square_y + square_size),
                         (square_x + square_size, square_y + square_size), 3)

        # Draw the spawn square
        spawn_square_size = 50
        spawn_square_pos = (152, 52)
        pygame.draw.rect(window, BLUE, (spawn_square_pos[0], spawn_square_pos[1], spawn_square_size, spawn_square_size))

        # Draw the finish square
        finish_square_size = 50
        finish_square_pos = (599, 499)
        pygame.draw.rect(window, BLUE,
                         (finish_square_pos[0], finish_square_pos[1], finish_square_size, finish_square_size))

        # Draw the green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw the coins
        for coin_pos in coins:
            if coin_pos != (625, 525):
                pygame.draw.circle(window, GOLD, coin_pos, coin_radius)

        # Draw red squares for each gold coin
        for orbiting_square in coin_orbiting_squares:
            orbiting_square.update_position()
            orbiting_square.draw(window)

        # Clear area where coin count text is rendered
        window.fill(LIGHT_BLUE, (0, 0, 200, 40))

        # Update coin count text surface
        coin_text = font.render(f"Coins: {coin_count}", True, BLACK)

        # Display text for coin count, attempts count, and current level
        window.blit(coin_text, (20, 20))

        attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
        window.blit(attempts_text, (window_width // 2 - 60, 20))

        level_text = font.render(f"Level: {current_level}/4", True, BLACK)
        window.blit(level_text, (window_width - 130, 20))

        # Update display
        pygame.display.flip()

# Level 2
def level_2():
    global circle_x, circle_y, circle_radius, current_level, coin_count, attempts
    attempts = 0
    coin_count = 0

    # Set up level 2
    rect_width_level2 = 600
    rect_height_level2 = 400
    rect_x_level2 = (window_width - rect_width_level2) // 2
    rect_y_level2 = (window_height - rect_height_level2) // 2

    # Set up circle
    circle_x = 100
    circle_y = 500
    circle_speed = 0.1

    # Set up gold coins
    coin_radius = 10
    coin_positions_level2 = [
        (200, 300),
        (110, 110),
        (200, 450),
        (400, 150),
        (400, 300),
        (400, 450),
        (600, 450),
        (690, 490),
        (600, 300),
        (675, 125),
    ]

    # Make (625, 125) coin larger
    larger_coin_radius = 20
    coin_positions_level2[-1] = (675, 125)

    # Obstacle 1
    obstacle1_size = 50
    obstacle1_x = 50
    obstacle1_y = 275
    obstacle1_speed = 0.8
    obstacle1_direction = 1

    # Obstacle 2
    obstacle2_size = 50
    obstacle2_x = 400
    obstacle2_y = 430
    obstacle2_speed = 0.3
    obstacle2_direction = 1

    # Obstacle 3
    obstacle3_size = 50
    obstacle3_x = 375
    obstacle3_y = 100
    obstacle3_speed = 0.4
    obstacle3_direction = 1

    # Obstacle 4
    obstacle4_size = 50
    obstacle4_x = 500
    obstacle4_y = 130
    obstacle4_speed = 0.3
    obstacle4_direction = 1

    # Buffer distance
    buffer_distance = 150

    # Main loop
    while current_level == 2:

        window.fill(LIGHT_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed, rect_x_level2, rect_y_level2,
                                                rect_width_level2, rect_height_level2)

        # Check for collision with the gold coins
        for coin_pos in coin_positions_level2:
            coin_x, coin_y = coin_pos
            if (circle_x + circle_radius > coin_x - coin_radius and circle_x - circle_radius < coin_x + coin_radius
                    and circle_y + circle_radius > coin_y - coin_radius and circle_y - circle_radius < coin_y + coin_radius):
                coin_positions_level2.remove(coin_pos)
                coin_count += 1
                if len(coin_positions_level2) == 0:
                    current_level = 3
                break

        # Check for collision with obstacles only if shift key is not pressed
        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
        if not shift_pressed:

            obstacle1_x += obstacle1_speed * obstacle1_direction
            if obstacle1_x <= 0 or obstacle1_x >= window_width - obstacle1_size:
                obstacle1_direction *= -1

            # Update obstacle2 position
            obstacle2_x += obstacle2_speed * obstacle2_direction
            if obstacle2_x <= buffer_distance or obstacle2_x >= window_width - obstacle2_size - buffer_distance:
                obstacle2_direction *= -1

            # Update obstacle3 position
            obstacle3_y += obstacle3_speed * obstacle3_direction
            if obstacle3_y <= 0 or obstacle3_y >= window_height - obstacle3_size:
                obstacle3_direction *= -1

            # Update obstacle4 position
            obstacle4_x += obstacle4_speed * obstacle4_direction
            if obstacle4_x <= buffer_distance or obstacle4_x >= window_width - obstacle4_size - buffer_distance:
                obstacle4_direction *= -1

            circle_rect = pygame.Rect(circle_x - circle_radius, circle_y - circle_radius, 2 * circle_radius,
                                      2 * circle_radius)
            obstacle_rects = [
                pygame.Rect(obstacle1_x, obstacle1_y, obstacle1_size, obstacle1_size),
                pygame.Rect(obstacle2_x, obstacle2_y, obstacle2_size, obstacle2_size),
                pygame.Rect(obstacle3_x, obstacle3_y, obstacle3_size, obstacle3_size),
                pygame.Rect(obstacle4_x, obstacle4_y, obstacle4_size, obstacle4_size)
            ]
            for obstacle_rect in obstacle_rects:
                if circle_rect.colliderect(obstacle_rect):
                    # Reset player position and coin count
                    circle_x = spawn_square_pos[0] + spawn_square_size // 2
                    circle_y = spawn_square_pos[1] + spawn_square_size // 2
                    coin_count = 0
                    death_sound.play()
                    attempts += 1
                    # Respawn coins
                    coin_positions_level2 = [
                        (200, 300),
                        (110, 110),
                        (200, 450),
                        (400, 150),
                        (400, 300),
                        (400, 450),
                        (600, 450),
                        (690, 490),
                        (600, 300),
                        (675, 125),
                    ]
                    coin_positions_level2[-1] = (675, 125)
                    break

        # Draw the rectangle for level 2
        pygame.draw.rect(window, (255, 255, 255),
                         (rect_x_level2, rect_y_level2, rect_width_level2, rect_height_level2))

        # Draw black lines on perimeter of the rectangle
        pygame.draw.line(window, BLACK, (rect_x_level2, rect_y_level2),
                         (rect_x_level2 + rect_width_level2, rect_y_level2), 3)
        pygame.draw.line(window, BLACK, (rect_x_level2, rect_y_level2),
                         (rect_x_level2, rect_y_level2 + rect_height_level2), 3)
        pygame.draw.line(window, BLACK, (rect_x_level2 + rect_width_level2, rect_y_level2),
                         (rect_x_level2 + rect_width_level2, rect_y_level2 + rect_height_level2), 3)
        pygame.draw.line(window, BLACK, (rect_x_level2, rect_y_level2 + rect_height_level2),
                         (rect_x_level2 + rect_width_level2, rect_y_level2 + rect_height_level2), 3)

        # Draw the spawn square
        spawn_square_size = 50
        spawn_square_pos = (101, 450)
        pygame.draw.rect(window, BLUE,
                         (spawn_square_pos[0], spawn_square_pos[1], spawn_square_size, spawn_square_size))

        # Draw the finish square
        finish_square_size = 50
        finish_square_pos = (650, 100)
        pygame.draw.rect(window, BLUE,
                         (finish_square_pos[0], finish_square_pos[1], finish_square_size, finish_square_size))

        # Draw green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw coins
        for pos in coin_positions_level2:
            if pos == (675, 125):
                continue
            if pos == (675, 125):
                pygame.draw.circle(window, GOLD, pos, larger_coin_radius)
            else:
                pygame.draw.circle(window, GOLD, pos, coin_radius)

        # Draw red square obstacle
        pygame.draw.rect(window, RED,
                         (obstacle1_x, obstacle1_y, obstacle1_size, obstacle1_size))  # Draw the first obstacle
        pygame.draw.rect(window, RED,
                         (obstacle2_x, obstacle2_y, obstacle2_size, obstacle2_size))  # Draw the second obstacle
        pygame.draw.rect(window, RED,
                         (obstacle3_x, obstacle3_y, obstacle3_size, obstacle3_size))  # Draw the third obstacle
        pygame.draw.rect(window, RED,
                         (obstacle4_x, obstacle4_y, obstacle4_size, obstacle4_size))  # Draw the fourth obstacle

        # Display text for coin count, attempts count, and current level
        coin_text = font.render(f"Coins: {coin_count}", True, BLACK)
        window.blit(coin_text, (20, 20))

        attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
        window.blit(attempts_text, (window_width // 2 - 60, 20))

        level_text = font.render(f"Level: {current_level}/4", True, BLACK)
        window.blit(level_text, (window_width - 130, 20))

        # Update display
        pygame.display.flip()

# Level 3
def level_3():
    global circle_x, circle_y, circle_radius, current_level, coin_count, attempts, coin_collected
    attempts = 0
    coin_count = 0
    coin_collected = False

    # Set up level 3
    circle_x = 395
    circle_y = 60
    circle_speed = 0.1

    # Position and size of rectangle
    rect_width = 300
    rect_height = 500
    rect_x = 250
    rect_y = 50

    # Set up gold coins
    coin_size = 10
    coin_positions_level3 = [
        (395, 100),
        (395, 150),
        (395, 200),
        (395, 250),
        (395, 300),
        (395, 350),
        (395, 400),
        (395, 450),
        (395, 500),
        (395, 530),
    ]

    # Set up red squares
    square_size = 15
    square_positions_level3 = [
        (300, 100, 0.11),
        (300, 150, 0.12),
        (300, 200, 0.13),
        (300, 250, 0.14),
        (300, 300, 0.15),
        (300, 350, 0.16),
        (300, 400, 0.17),
        (300, 450, 0.18),
        (300, 500, 0.19),
    ]

    # Main loop
    while current_level == 3:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses
        keys = pygame.key.get_pressed()
        ignore_collision = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        if not ignore_collision:
            circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed)

        # Movement even if shift is pressed
        if keys[pygame.K_LEFT]:
            circle_x -= circle_speed
        if keys[pygame.K_RIGHT]:
            circle_x += circle_speed
        if keys[pygame.K_UP]:
            circle_y -= circle_speed
        if keys[pygame.K_DOWN]:
            circle_y += circle_speed

        # Check for collision with black lines
        if (circle_x - circle_radius <= rect_x or circle_x + circle_radius >= rect_x + rect_width or
                circle_y - circle_radius <= rect_y or circle_y + circle_radius >= rect_y + rect_height):
            # Prevent movement in collided direction
            if circle_x - circle_radius <= rect_x:
                circle_x = rect_x + circle_radius
            elif circle_x + circle_radius >= rect_x + rect_width:
                circle_x = rect_x + rect_width - circle_radius
            if circle_y - circle_radius <= rect_y:
                circle_y = rect_y + circle_radius
            elif circle_y + circle_radius >= rect_y + rect_height:
                circle_y = rect_y + rect_height - circle_radius

        # Check for collision with the red squares, only if collision is not ignored
        if not ignore_collision:
            for square_x, square_y, _ in square_positions_level3:
                distance = math.sqrt((circle_x - square_x) ** 2 + (circle_y - square_y) ** 2)
                if distance < circle_radius + square_size / 2:
                    # Collision detected, reset player position
                    circle_x = 395
                    circle_y = 60
                    death_sound.play()
                    attempts += 1
                    coin_count = 0

                    coin_positions_level3 = [
                        (395, 100),
                        (395, 150),
                        (395, 200),
                        (395, 250),
                        (395, 300),
                        (395, 350),
                        (395, 400),
                        (395, 450),
                        (395, 500),
                        (395, 530),
                    ]

        # Check for collision with gold coins
        for coin_pos in coin_positions_level3:
            coin_x, coin_y = coin_pos
            if (circle_x + circle_radius > coin_x - coin_size / 2 and circle_x - circle_radius < coin_x + coin_size / 2
                    and circle_y + circle_radius > coin_y - coin_size / 2 and circle_y - circle_radius < coin_y + coin_size / 2):
                if coin_pos == (395, 530):
                    coin_positions_level3.remove(coin_pos)
                else:
                    coin_positions_level3.remove(coin_pos)
                    coin_count += 1

                if len(coin_positions_level3) == 0:
                    current_level = 4
                break

        # Draw rectangle
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(rect_x, rect_y, rect_width, rect_height))

        # Draw black lines around the rectangle
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x + rect_width, rect_y), 3)
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x, rect_y + rect_height), 3)
        pygame.draw.line(window, BLACK, (rect_x + rect_width, rect_y),
                         (rect_x + rect_width, rect_y + rect_height), 3)
        pygame.draw.line(window, BLACK, (rect_x, rect_y + rect_height),
                         (rect_x + rect_width, rect_y + rect_height), 3)

        # Update red squares position
        for i, (square_x, square_y, velocity) in enumerate(square_positions_level3):
            # Move square horizontally
            square_x += velocity
            # Check if the square reached the boundaries
            if square_x - square_size // 2 <= rect_x or square_x + square_size // 2 >= rect_x + rect_width:
                # Reverse direciton
                velocity *= -1
            # Update square
            square_positions_level3[i] = (square_x, square_y, velocity)

        # Draw the spawn square
        spawn_square_size = 50
        spawn_square_pos = (370, 50)
        pygame.draw.rect(window, BLUE,
                         (spawn_square_pos[0], spawn_square_pos[1], spawn_square_size, spawn_square_size))

        # Draw the finish square
        finish_square_size = 50
        finish_square_pos = (370, 500)
        pygame.draw.rect(window, BLUE,
                         (finish_square_pos[0], finish_square_pos[1], finish_square_size, finish_square_size))

        # Draw green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw the red squares
        for square_x, square_y, _ in square_positions_level3:
            pygame.draw.rect(window, RED,
                             (square_x - square_size // 2, square_y - square_size // 2, square_size, square_size))

        # Draw gold coins
        for coin_pos in coin_positions_level3:
            if coin_pos != (395, 530):
                pygame.draw.circle(window, GOLD, coin_pos, coin_size)

        # Clear the area where the text is rendered
        window.fill(LIGHT_BLUE, (0, 0, window_width, 40))

        # Update all text surfaces
        coin_text = font.render(f"Coins: {coin_count}", True, BLACK)
        attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
        level_text = font.render(f"Level: {current_level}/4", True, BLACK)

        # Display all text elements
        window.blit(coin_text, (20, 20))
        window.blit(attempts_text, (window_width // 2 - 60, 20))
        window.blit(level_text, (window_width - 130, 20))

        # Update display
        pygame.display.flip()

# Level 4
def level_4():
    global circle_x, circle_y, circle_radius, current_level, coin_collected, attempts, coin_radius

    coin_radius = 10
    coin_count = 0
    respawn_coins = True
    checkpoint_reached = False
    respawn_specific_coins = True
    coin_collected = False

    # Set up level 4
    circle_x = 70
    circle_y = 380
    circle_speed = 0.1

    # Position and size of rectangle
    rect_width = 700
    rect_height = 200
    rect_x = (window_width - rect_width) // 2
    rect_y = (window_height - rect_height) // 2

    # Set up gold coins
    initial_coin_positions_level4 = [
        (120, 300),
        (210, 300),
        (300, 300),
        (510, 300),
        (610, 300),
        (700, 300),
        (725, 225, 10),
    ]
    coin_positions_level4 = initial_coin_positions_level4.copy()

    # Set up red squares
    square_size = 15
    square_positions_level4 = [
        (121, 300, 0.11),
        (211, 300, 0.12),
        (301, 300, 0.13),
        (511, 300, 0.14),
        (611, 300, 0.15),
        (690, 350, 0.16),
    ]

    # Main loop
    while current_level == 4:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed)

        # Check for collision with gold coins
        for coin_pos in coin_positions_level4:
            if not coin_collected and circle_x + circle_radius > coin_pos[0] and circle_x - circle_radius < coin_pos[
                0] + coin_radius \
                    and circle_y + circle_radius > coin_pos[1] and circle_y - circle_radius < coin_pos[1] + coin_radius:
                coin_positions_level4.remove(coin_pos)
                coin_count += 1
                if not coin_positions_level4:
                    coin_collected = True
                    respawn_coins = False
                    victory_screen()

        # Check for collision with black lines
        if (circle_x - circle_radius <= rect_x or circle_x + circle_radius >= rect_x + rect_width or
                circle_y - circle_radius <= rect_y or circle_y + circle_radius >= rect_y + rect_height):
            # Prevent movement in collided direction
            if circle_x - circle_radius <= rect_x:
                circle_x = rect_x + circle_radius
            elif circle_x + circle_radius >= rect_x + rect_width:
                circle_x = rect_x + rect_width - circle_radius
            if circle_y - circle_radius <= rect_y:
                circle_y = rect_y + circle_radius
            elif circle_y + circle_radius >= rect_y + rect_height:
                circle_y = rect_y + rect_height - circle_radius

        # Check for collision with red squares, unless Shift key is pressed
        if not pygame.key.get_pressed()[pygame.K_LSHIFT] and not pygame.key.get_pressed()[pygame.K_RSHIFT]:
            for square_x, square_y, _ in square_positions_level4:
                distance = math.sqrt((circle_x - square_x) ** 2 + (circle_y - square_y) ** 2)
                if distance < circle_radius + square_size / 2:

                    if coin_count >= 3:
                        if not checkpoint_reached:
                            circle_x = 70
                            circle_y = 380
                        else:
                            circle_x = 400
                            circle_y = 300
                            respawn_coins = False
                            if respawn_specific_coins:
                                respawn_specific_coins = False
                                coin_positions_level4 = initial_coin_positions_level4.copy()
                        attempts += 1
                        death_sound.play()
                    else:
                        circle_x = 70
                        circle_y = 380
                        coin_count = 0
                        attempts += 1
                        death_sound.play()
                    checkpoint_reached = False
                    coin_positions_level4 = initial_coin_positions_level4.copy()

                # Check for collision with checkpoint square
            if (circle_x + circle_radius >= 380 and circle_y + circle_radius >= 200 and
                    circle_x - circle_radius <= 430 and circle_y - circle_radius <= 400):
                checkpoint_reached = True
                if checkpoint_reached:
                    coin_positions_level4 = [pos for pos in coin_positions_level4 if
                                             pos not in [(120, 300), (210, 300), (300, 300)]]
                    coin_count = 3

        # Draw rectangle
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(rect_x, rect_y, rect_width, rect_height))

        # Draw black lines around rectangle
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x + rect_width, rect_y), 3)
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x, rect_y + rect_height), 3)
        pygame.draw.line(window, BLACK, (rect_x + rect_width, rect_y),
                         (rect_x + rect_width, rect_y + rect_height), 3)
        pygame.draw.line(window, BLACK, (rect_x, rect_y + rect_height),
                         (rect_x + rect_width, rect_y + rect_height), 3)

        # Update red squares position
        for i, (square_x, square_y, velocity) in enumerate(square_positions_level4):
            # Move square vertically
            square_y += velocity
            # Check if square reached boundaries
            if square_y - square_size // 2 <= rect_y or square_y + square_size // 2 >= rect_y + rect_height:
                # Reverse direction
                velocity *= -1
            # Update the position and velocity of square
            square_positions_level4[i] = (square_x, square_y, velocity)

            # Draw red square
            pygame.draw.rect(window, RED,
                             (square_x - square_size // 2, square_y - square_size // 2, square_size, square_size))

        # Draw the spawn square
        spawn_square_size = 50
        spawn_square_pos = (52, 349)
        pygame.draw.rect(window, BLUE,
                         (spawn_square_pos[0], spawn_square_pos[1], spawn_square_size, spawn_square_size))

        # Draw the checkpoint square
        spawn_square_width = 50
        spawn_square_height = 200
        spawn_square_pos = (380, 200)
        pygame.draw.rect(window, BLUE,
                         (spawn_square_pos[0], spawn_square_pos[1], spawn_square_width, spawn_square_height))

        # Draw the finish square
        finish_square_size = 50
        finish_square_pos = (700, 202)
        pygame.draw.rect(window, BLUE,
                         (finish_square_pos[0], finish_square_pos[1], finish_square_size, finish_square_size))

        # Draw green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw gold coins for level 4 if not collected
        if coin_positions_level4:
            for coin_pos in coin_positions_level4:
                if isinstance(coin_pos, tuple) and len(coin_pos) == 2:
                    pygame.draw.circle(window, GOLD, coin_pos, coin_radius)

        # Clear the area where the text is rendered
        window.fill(LIGHT_BLUE, (0, 0, window_width, 40))

        # Update all text surfaces
        coin_text = font.render(f"Coins: {coin_count}", True, BLACK)
        attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
        level_text = font.render(f"Level: {current_level}/4", True, BLACK)

        # Display all text elements
        window.blit(coin_text, (20, 20))
        window.blit(attempts_text, (window_width // 2 - 60, 20))
        window.blit(level_text, (window_width - 130, 20))

        # Update the display
        pygame.display.flip()

    # Display victory
    if current_level == 4:
        victory_screen()

def victory_screen():
    # Fill screen with light blue
    window.fill(LIGHT_BLUE)

    # Display "You Win!"
    font = pygame.font.Font(None, 36)
    text = font.render("You Win!", True, BLACK)
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2 - 50))
    window.blit(text, text_rect)

    # Draw restart button
    restart_button_rect = pygame.Rect(window_width // 2 - 50, window_height // 2 + 50, 100, 40)
    pygame.draw.rect(window, GREEN, restart_button_rect)
    font = pygame.font.Font(None, 24)
    restart_text = font.render("Restart", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    window.blit(restart_text, restart_text_rect)

    # Update the display
    pygame.display.flip()

    # Stay victory screen until player chooses to restart or exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_pos):
                    reset_levels()
                    current_level = 1
                    return

def reset_levels():
    global current_level, circle_x, circle_y, coin_x, coin_y, coin_collected_level1, coin_collected_level2, coin_collected_level3, coin_collected_level4, coin_collected_level5

    # Reset player position for all levels
    circle_x = window_width // 2
    circle_y = window_height // 2

    # Reset coin collected status for all levels
    coin_collected_level1 = False
    coin_collected_level2 = False
    coin_collected_level3 = False
    coin_collected_level4 = False

    # Reset current level to 1
    current_level = 1


# Main game loop
while True:
    # Fill background with light blue
    window.fill(LIGHT_BLUE)

    if current_level == 1:
        level_1()
    elif current_level == 2:
        level_2()
    elif current_level == 3:
        level_3()
    elif current_level == 4:
        level_4()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()