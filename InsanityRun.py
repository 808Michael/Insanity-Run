import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Game")

# Set up the colors
LIGHT_BLUE = (173, 216, 230)  # Light blue color
BLUE = (100, 149, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)  # Gold color

# Global variables
circle_radius = 10
current_level = 1
coin_count = 0
attempts = 0

# Define font
font = pygame.font.SysFont("times new roman", 20)

# Initialize the mixer module
pygame.mixer.init()

# Load the sound file
pygame.mixer.music.load('mp3/535331_Stay-Inside-Me.mp3')
death_sound = pygame.mixer.Sound('mp3/geometry-dash-death-sound-effect.mp3')

# Set the volume level (optional)
pygame.mixer.music.set_volume(0.5)  # Adjust volume level between 0.0 and 1.0

# Start playing the sound on a loop
pygame.mixer.music.play(loops=-1)  # Set loops to -1 for infinite looping


# Function to generate a random position within the square
def generate_random_position(square_x, square_y, square_size, coin_size):
    return random.randint(square_x, square_x + square_size - coin_size), random.randint(square_y,
                                                                                        square_y + square_size - coin_size)


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
        self.size = size  # Size of the square
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
    global circle_x, circle_y, coins, circle_radius, current_level, coin_count
    attempts = 0

    # Set up the square
    square_size = 500
    square_x = 150
    square_y = 50

    # Set up the circle (player spawn location)
    circle_x = 175  # Set the player spawn location x-coordinate
    circle_y = 75  # Set the player spawn location y-coordinate
    circle_speed = 0.1

    # Set up the gold coins
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
    initial_coin_positions = coins[:]  # Copy the initial positions

    # Create a list to store OrbitingSquare instances for each gold coin
    coin_orbiting_squares = []
    for coin_pos in coins[:-1]:
        coin_orbiting_squares.append(OrbitingSquare(center=coin_pos, angle_offset=0, radius=30, size=20))

    # Main loop
    while current_level == 1:
        # Clear the window surface
        window.fill(LIGHT_BLUE)

        # Check if the Shift key is being held down
        keys = pygame.key.get_pressed()
        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed, square_x, square_y, square_size,
                                                square_size)

        # Check for collision with the gold coins
        for coin_pos in coins:
            coin_x, coin_y = coin_pos
            if (circle_x + circle_radius > coin_x - coin_radius and circle_x - circle_radius < coin_x + coin_radius
                    and circle_y + circle_radius > coin_y - coin_radius and circle_y - circle_radius < coin_y + coin_radius):
                coins.remove(coin_pos)
                coin_count += 1  # Increment the coin counter
                if len(coins) == 0:  # No coins left, transition to level 2
                    current_level = 2
                break

        # Check for collision with the player square
        for orbiting_square in coin_orbiting_squares:
            if (circle_x + circle_radius > orbiting_square.x - 5 and circle_x - circle_radius < orbiting_square.x + 5
                    and circle_y + circle_radius > orbiting_square.y - 5 and circle_y - circle_radius < orbiting_square.y + 5):
                # Collision occurred, handle accordingly (e.g., decrease attempts)
                if not shift_pressed:  # Check if Shift key is not pressed
                    death_sound.play()
                    attempts += 1
                    # Reset player position to spawn location
                    circle_x = 170
                    circle_y = 70
                    # Respawn all coins on the screen
                    coins = initial_coin_positions[:]

        # Draw the larger white square
        pygame.draw.rect(window, (255, 255, 255), (square_x, square_y, square_size, square_size))

        # Draw black lines on the perimeter of the white square
        pygame.draw.line(window, BLACK, (square_x, square_y), (square_x + square_size, square_y), 3)  # Top line
        pygame.draw.line(window, BLACK, (square_x, square_y), (square_x, square_y + square_size), 3)  # Left line
        pygame.draw.line(window, BLACK, (square_x + square_size, square_y),
                         (square_x + square_size, square_y + square_size), 3)  # Right line
        pygame.draw.line(window, BLACK, (square_x, square_y + square_size),
                         (square_x + square_size, square_y + square_size), 3)  # Bottom line

        # Draw the spawn square (blue square)
        spawn_square_size = 50
        spawn_square_pos = (152, 52)
        pygame.draw.rect(window, BLUE, (spawn_square_pos[0], spawn_square_pos[1], spawn_square_size, spawn_square_size))

        # Draw the finish square (blue square)
        finish_square_size = 50
        finish_square_pos = (599, 499)
        pygame.draw.rect(window, BLUE,
                         (finish_square_pos[0], finish_square_pos[1], finish_square_size, finish_square_size))

        # Draw the green circle (player)
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw the gold coins
        for coin_pos in coins:
            if coin_pos != (625, 525):  # Skip drawing the coin at (625, 525)
                pygame.draw.circle(window, GOLD, coin_pos, coin_radius)

        # Draw the red squares for each gold coin
        for orbiting_square in coin_orbiting_squares:
            orbiting_square.update_position()  # Update position
            orbiting_square.draw(window)  # Draw

        # Clear the area where the coin count text is rendered
        window.fill(LIGHT_BLUE, (0, 0, 200, 40))

        # Update the coin count text surface
        coin_text = font.render(f"Coins: {coin_count}", True, BLACK)

        # Display text for coin count, attempts count, and current level
        window.blit(coin_text, (20, 20))

        attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
        window.blit(attempts_text, (window_width // 2 - 60, 20))

        level_text = font.render(f"Level: {current_level}/5", True, BLACK)
        window.blit(level_text, (window_width - 130, 20))

        # Update the display
        pygame.display.flip()


# Level 2
def level_2():
    global circle_x, circle_y, circle_radius, current_level, coin_count
    attempts = 0  # Initialize attempts count for level 2
    coin_count = 0  # Initialize coin count for level 2

    # Set up level 2
    rect_width_level2 = 600
    rect_height_level2 = 400
    rect_x_level2 = (window_width - rect_width_level2) // 2
    rect_y_level2 = (window_height - rect_height_level2) // 2

    # Set up the circle
    circle_x = 100
    circle_y = 500
    circle_speed = 0.25

    # Set up the gold coins for level 2
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

    # Make the coin at (625, 125) larger
    larger_coin_radius = 20
    coin_positions_level2[-1] = (675, 125)

    # Set up the red square obstacle 1
    obstacle1_size = 50
    obstacle1_x = 50
    obstacle1_y = 275
    obstacle1_speed = 1
    obstacle1_direction = 1  # 1 for moving right, -1 for moving left

    # Set up the second red square obstacle
    obstacle2_size = 50
    obstacle2_x = 400
    obstacle2_y = 430
    obstacle2_speed = 0.3  # Adjust the speed
    obstacle2_direction = 1  # 1 for moving right, -1 for moving left

    # Set up the third red square obstacle (moving up and down)
    obstacle3_size = 50
    obstacle3_x = 375
    obstacle3_y = 100
    obstacle3_speed = 0.4  # Adjust the speed
    obstacle3_direction = 1  # 1 for moving down, -1 for moving up

    # Set up the fourth red square obstacle (moving left and right)
    obstacle4_size = 50
    obstacle4_x = 500
    obstacle4_y = 130
    obstacle4_speed = 0.3  # Adjust the speed
    obstacle4_direction = 1  # 1 for moving right, -1 for moving left

    # Main loop for level 2
    while current_level == 2:
        # Clear the window surface
        window.fill(LIGHT_BLUE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses and collision with rectangle
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed, rect_x_level2, rect_y_level2,
                                                rect_width_level2, rect_height_level2)

        # Check for collision with the gold coins
        for coin_pos in coin_positions_level2:
            coin_x, coin_y = coin_pos
            if (circle_x + circle_radius > coin_x - coin_radius and circle_x - circle_radius < coin_x + coin_radius
                    and circle_y + circle_radius > coin_y - coin_radius and circle_y - circle_radius < coin_y + coin_radius):
                coin_positions_level2.remove(coin_pos)
                coin_count += 1  # Increment the coin counter
                if len(coin_positions_level2) == 0:  # No coins left, transition to level 3
                    current_level = 3
                break

        # Check for collision with obstacles only if shift key is not pressed
        shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
        if not shift_pressed:
            # Update obstacle positions regardless of collision
            obstacle1_x += obstacle1_speed * obstacle1_direction
            if obstacle1_x <= 0 or obstacle1_x >= window_width - obstacle1_size:
                obstacle1_direction *= -1  # Change direction when hitting the window edge

            # Update obstacle2 position
            obstacle2_x += obstacle2_speed * obstacle2_direction
            if obstacle2_x <= 0 or obstacle2_x >= window_width - obstacle2_size:
                obstacle2_direction *= -1  # Change direction when hitting the window edge

            # Update obstacle3 position
            obstacle3_y += obstacle3_speed * obstacle3_direction
            if obstacle3_y <= 0 or obstacle3_y >= window_height - obstacle3_size:
                obstacle3_direction *= -1  # Change direction when hitting the window edge

            # Update obstacle4 position
            obstacle4_x += obstacle4_speed * obstacle4_direction
            if obstacle4_x <= 0 or obstacle4_x >= window_width - obstacle4_size:
                obstacle4_direction *= -1  # Change direction when hitting the window edge

        # Draw the rectangle for level 2
        pygame.draw.rect(window, (255, 255, 255),
                         (rect_x_level2, rect_y_level2, rect_width_level2, rect_height_level2))

        # Draw black lines on the perimeter of the rectangle
        pygame.draw.line(window, BLACK, (rect_x_level2, rect_y_level2),
                         (rect_x_level2 + rect_width_level2, rect_y_level2), 3)  # Top line
        pygame.draw.line(window, BLACK, (rect_x_level2, rect_y_level2),
                         (rect_x_level2, rect_y_level2 + rect_height_level2), 3)  # Left line
        pygame.draw.line(window, BLACK, (rect_x_level2 + rect_width_level2, rect_y_level2),
                         (rect_x_level2 + rect_width_level2, rect_y_level2 + rect_height_level2), 3)  # Right line
        pygame.draw.line(window, BLACK, (rect_x_level2, rect_y_level2 + rect_height_level2),
                         (rect_x_level2 + rect_width_level2, rect_y_level2 + rect_height_level2), 3)  # Bottom line

        # Draw the spawn square (blue square)
        spawn_square_size = 50
        spawn_square_pos = (101, 450)
        pygame.draw.rect(window, BLUE,
                         (spawn_square_pos[0], spawn_square_pos[1], spawn_square_size, spawn_square_size))

        # Draw the finish square (blue square)
        finish_square_size = 50
        finish_square_pos = (650, 100)
        pygame.draw.rect(window, BLUE,
                         (finish_square_pos[0], finish_square_pos[1], finish_square_size, finish_square_size))

        # Draw the green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw coins
        for pos in coin_positions_level2:
            if pos == (675, 125):
                continue  # Skip drawing this coin
            if pos == (675, 125):
                pygame.draw.circle(window, GOLD, pos, larger_coin_radius)
            else:
                pygame.draw.circle(window, GOLD, pos, coin_radius)

        # Draw the red square obstacle
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

        level_text = font.render(f"Level: {current_level}/5", True, BLACK)
        window.blit(level_text, (window_width - 130, 20))

        # Update the display
        pygame.display.flip()

# Level 3
def level_3():
    global circle_x, circle_y, circle_radius, current_level, coin_x_level3, coin_y_level3, coin_collected
    # Set up level 3
    # Set up the circle
    circle_x = window_width // 2
    circle_y = window_height // 2
    circle_speed = 0.25

    # Position and size of the rectangle
    rect_width = 300
    rect_height = 500
    rect_x = (window_width - rect_width) // 2  # Center the rectangle horizontally
    rect_y = (window_height - rect_height) // 2  # Center the rectangle vertically

    # Set up the gold coin for level 3
    coin_size = 20
    coin_x_level3 = 400
    coin_y_level3 = 400
    coin_collected = False

    # Main loop for level 3
    while current_level == 3:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed)

        # Check for collision with the gold coin
        if not coin_collected and circle_x + circle_radius > coin_x_level3 and circle_x - circle_radius < coin_x_level3 + coin_size \
                and circle_y + circle_radius > coin_y_level3 and circle_y - circle_radius < coin_y_level3 + coin_size:
            coin_collected = True
            # Transition to level 4
            current_level = 4

        # Check for collision with black lines
        if (circle_x - circle_radius <= rect_x or circle_x + circle_radius >= rect_x + rect_width or
                circle_y - circle_radius <= rect_y or circle_y + circle_radius >= rect_y + rect_height):
            # Prevent movement in the collided direction
            if circle_x - circle_radius <= rect_x:
                circle_x = rect_x + circle_radius
            elif circle_x + circle_radius >= rect_x + rect_width:
                circle_x = rect_x + rect_width - circle_radius
            if circle_y - circle_radius <= rect_y:
                circle_y = rect_y + circle_radius
            elif circle_y + circle_radius >= rect_y + rect_height:
                circle_y = rect_y + rect_height - circle_radius

        # Draw the rectangle
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(rect_x, rect_y, rect_width, rect_height))

        # Draw black lines around the rectangle
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x + rect_width, rect_y), 3)  # Top line
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x, rect_y + rect_height), 3)  # Left line
        pygame.draw.line(window, BLACK, (rect_x + rect_width, rect_y),
                         (rect_x + rect_width, rect_y + rect_height), 3)  # Right line
        pygame.draw.line(window, BLACK, (rect_x, rect_y + rect_height),
                         (rect_x + rect_width, rect_y + rect_height), 3)  # Bottom line

        # Draw the green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw the gold coin for level 3 as a circle
        pygame.draw.circle(window, GOLD, (coin_x_level3 + coin_size // 2, coin_y_level3 + coin_size // 2),
                           coin_size // 2)

        # Display text for coin count, attempts count, and current level
        coin_text = font.render(f"Coins: {coin_count}", True, BLACK)
        window.blit(coin_text, (20, 20))

        attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
        window.blit(attempts_text, (window_width // 2 - 60, 20))

        level_text = font.render(f"Level: {current_level}/5", True, BLACK)
        window.blit(level_text, (window_width - 130, 20))

        # Update the display
        pygame.display.flip()


# Level 4
def level_4():
    global circle_x, circle_y, circle_radius, current_level, coin_x_level4, coin_y_level4, coin_collected
    # Set up level 4
    # Set up the circle
    circle_x = window_width // 2
    circle_y = window_height // 2
    circle_speed = 0.25

    # Position and size of the rectangle
    rect_width = 700
    rect_height = 200
    rect_x = (window_width - rect_width) // 2  # Center the rectangle horizontally
    rect_y = (window_height - rect_height) // 2  # Center the rectangle vertically

    # Set up the gold coin for level 4
    coin_radius = 10  # Adjust the radius to make it smaller than the circle
    coin_x_level4 = 200
    coin_y_level4 = 300
    coin_collected = False

    # Main loop for level 4
    while current_level == 4:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed)

        # Check for collision with the gold coin
        if not coin_collected and circle_x + circle_radius > coin_x_level4 and circle_x - circle_radius < coin_x_level4 + coin_radius \
                and circle_y + circle_radius > coin_y_level4 and circle_y - circle_radius < coin_y_level4 + coin_radius:
            coin_collected = True
            # Transition to level 5 when the coin is collected
            current_level = 5

        # Check for collision with black lines
        if (circle_x - circle_radius <= rect_x or circle_x + circle_radius >= rect_x + rect_width or
                circle_y - circle_radius <= rect_y or circle_y + circle_radius >= rect_y + rect_height):
            # Prevent movement in the collided direction
            if circle_x - circle_radius <= rect_x:
                circle_x = rect_x + circle_radius
            elif circle_x + circle_radius >= rect_x + rect_width:
                circle_x = rect_x + rect_width - circle_radius
            if circle_y - circle_radius <= rect_y:
                circle_y = rect_y + circle_radius
            elif circle_y + circle_radius >= rect_y + rect_height:
                circle_y = rect_y + rect_height - circle_radius

        # Draw the rectangle
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(rect_x, rect_y, rect_width, rect_height))

        # Draw black lines around the rectangle
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x + rect_width, rect_y), 3)  # Top line
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x, rect_y + rect_height), 3)  # Left line
        pygame.draw.line(window, BLACK, (rect_x + rect_width, rect_y),
                         (rect_x + rect_width, rect_y + rect_height), 3)  # Right line
        pygame.draw.line(window, BLACK, (rect_x, rect_y + rect_height),
                         (rect_x + rect_width, rect_y + rect_height), 3)  # Bottom line

        # Draw the green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw the gold coin for level 4 if it's not collected
        if not coin_collected:
            pygame.draw.circle(window, GOLD, (coin_x_level4, coin_y_level4), coin_radius)

            # Display text for coin count, attempts count, and current level
            coin_text = font.render(f"Coins: {coin_count}", True, BLACK)
            window.blit(coin_text, (20, 20))

            attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
            window.blit(attempts_text, (window_width // 2 - 60, 20))

            level_text = font.render(f"Level: {current_level}/5", True, BLACK)
            window.blit(level_text, (window_width - 130, 20))

        # Update the display
        pygame.display.flip()


# Level 5
def level_5():
    global circle_x, circle_y, circle_radius, current_level, coin_x_level5, coin_y_level5, coin_collected
    # Set up level 5
    # Set up the circle
    circle_x = window_width // 2
    circle_y = window_height // 2
    circle_speed = 0.25

    # Position and size of the rectangle for Level 5
    rect_width = 400
    rect_height = 500
    rect_x = (window_width - rect_width) // 2  # Center the rectangle horizontally
    rect_y = (window_height - rect_height) // 2  # Center the rectangle vertically

    # Set up the gold coin for level 5
    coin_radius = 10  # Adjust the radius to make it smaller than the circle
    coin_x_level5 = 400
    coin_y_level5 = 400
    coin_collected = False

    # Main loop for level 5
    while current_level == 5:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed)

        # Check for collision with the gold coin
        if not coin_collected and circle_x + circle_radius > coin_x_level5 and circle_x - circle_radius < coin_x_level5 + coin_radius \
                and circle_y + circle_radius > coin_y_level5 and circle_y - circle_radius < coin_y_level5 + coin_radius:
            coin_collected = True

        # Check for collision with black lines
        if not coin_collected:
            if (circle_x - circle_radius <= rect_x or circle_x + circle_radius >= rect_x + rect_width or
                    circle_y - circle_radius <= rect_y or circle_y + circle_radius >= rect_y + rect_height):
                # Prevent movement in the collided direction
                if circle_x - circle_radius <= rect_x:
                    circle_x = rect_x + circle_radius
                elif circle_x + circle_radius >= rect_x + rect_width:
                    circle_x = rect_x + rect_width - circle_radius
                if circle_y - circle_radius <= rect_y:
                    circle_y = rect_y + circle_radius
                elif circle_y + circle_radius >= rect_y + rect_height:
                    circle_y = rect_y + rect_height - circle_radius

        # Draw the rectangle for Level 5
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(rect_x, rect_y, rect_width, rect_height))

        # Draw black lines around the rectangle for Level 5
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x + rect_width, rect_y), 3)  # Top line
        pygame.draw.line(window, BLACK, (rect_x, rect_y), (rect_x, rect_y + rect_height), 3)  # Left line
        pygame.draw.line(window, BLACK, (rect_x + rect_width, rect_y),
                         (rect_x + rect_width, rect_y + rect_height), 3)  # Right line
        pygame.draw.line(window, BLACK, (rect_x, rect_y + rect_height),
                         (rect_x + rect_width, rect_y + rect_height), 3)  # Bottom line

        # Draw the green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw the gold coin for level 5 if it's not collected
        if not coin_collected:
            pygame.draw.circle(window, GOLD, (coin_x_level5, coin_y_level5), coin_radius)

            # Display text for coin count, attempts count, and current level
            coin_text = font.render(f"Coins: {coin_count}", True, BLACK)
            window.blit(coin_text, (20, 20))

            attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
            window.blit(attempts_text, (window_width // 2 - 60, 20))

            level_text = font.render(f"Level: {current_level}/5", True, BLACK)
            window.blit(level_text, (window_width - 130, 20))

        else:
            # Call the victory_screen function
            victory_screen()
            # Break out of the main game loop
            break

        # Update the display
        pygame.display.flip()


def victory_screen():
    # Fill the screen with light blue
    window.fill(LIGHT_BLUE)

    # Display "You Win!" message
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

    # Stay on the victory screen until the player chooses to restart or exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_pos):
                    # Restart the game by resetting all levels to level 1
                    reset_levels()
                    # Start from level 1
                    current_level = 1
                    # Return to the main game loop
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
    coin_collected_level5 = False

    # Reset current level to 1
    current_level = 1


# Main game loop
while True:
    # Fill the background with light blue
    window.fill(LIGHT_BLUE)

    if current_level == 1:
        level_1()
    elif current_level == 2:
        level_2()
    elif current_level == 3:
        level_3()
    elif current_level == 4:
        level_4()
    elif current_level == 5:
        level_5()

    # Update the display
    pygame.display.flip()

    # Event handling for quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()