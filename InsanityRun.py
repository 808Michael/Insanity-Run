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
pygame.display.set_caption("Insanity Run")

# Set up the colors
LIGHT_BLUE = (173, 216, 230)  # Light blue color
BLUE = (100, 149, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)  # Gold color

# Global variables
circle_radius = 10
current_level = 1
coin_count = 0
attempts = 0

# Define font
font = pygame.font.SysFont("times new roman", 20)

# Function to generate a random position within the square
def generate_random_position(square_x, square_y, square_size, coin_size):
    return random.randint(square_x, square_x + square_size - coin_size), random.randint(square_y, square_y + square_size - coin_size)

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

# Level 1
def level_1():
    global circle_x, circle_y, coins, circle_radius, current_level, coin_count
    attempts = 0
    # Set up the square
    square_size = 500
    square_x = 150
    square_y = 50

    # Set up the circle
    circle_x = 170
    circle_y = 70
    circle_speed = 0.25

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
        (600, 500),
        (500, 400),
    ]
    coins = coin_positions

    # Set up the red squares
    red_squares = [
        pygame.Rect(263, 163, 15, 15),
        pygame.Rect(363, 63, 15, 15),
        pygame.Rect(563, 63, 15, 15),
        pygame.Rect(163, 263, 15, 15),
        pygame.Rect(363, 263, 15, 15),
        pygame.Rect(563, 263, 15, 15),
        pygame.Rect(163, 463, 15, 15),
        pygame.Rect(363, 463, 15, 15),
        pygame.Rect(563, 463, 15, 15),
        pygame.Rect(463, 363, 15, 15),
    ]

    # Main loop
    while current_level == 1:
        # Clear the window surface
        window.fill(LIGHT_BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed, square_x, square_y, square_size, square_size)

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

        # Check for collision with red squares
        for square in red_squares:
            if square.colliderect(pygame.Rect(circle_x - circle_radius, circle_y - circle_radius, 2 * circle_radius,
                                              2 * circle_radius)):
                # Collision detected with red square, increase attempts
                attempts += 1

                # Reset circle position
                circle_x = 170
                circle_y = 70

        # Draw the larger white square
        pygame.draw.rect(window, (255, 255, 255), (square_x, square_y, square_size, square_size))

        # Draw black lines on the perimeter of the white square
        pygame.draw.line(window, BLACK, (square_x, square_y), (square_x + square_size, square_y), 3)  # Top line
        pygame.draw.line(window, BLACK, (square_x, square_y), (square_x, square_y + square_size), 3)  # Left line
        pygame.draw.line(window, BLACK, (square_x + square_size, square_y),
                         (square_x + square_size, square_y + square_size), 3)  # Right line
        pygame.draw.line(window, BLACK, (square_x, square_y + square_size),
                         (square_x + square_size, square_y + square_size), 3)  # Bottom line

        # Draw the green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw the gold coins
        for coin_pos in coins:
            pygame.draw.circle(window, GOLD, coin_pos, coin_radius)

        # Draw the red squares
        for square in red_squares:
            pygame.draw.rect(window, RED, square)

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
    global circle_x, circle_y, circle_radius, current_level, coin_x_level2, coin_y_level2
    # Set up level 2
    rect_width_level2 = 600
    rect_height_level2 = 400
    rect_x_level2 = (window_width - rect_width_level2) // 2
    rect_y_level2 = (window_height - rect_height_level2) // 2

    # Set up the circle
    circle_x = window_width // 2
    circle_y = window_height // 2
    circle_speed = 0.25

    # Set up the gold coin for level 2
    coin_size = 20
    coin_x_level2 = 200
    coin_y_level2 = 200

    # Main loop for level 2
    while current_level == 2:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses and collision with rectangle
        circle_x, circle_y = handle_key_presses(circle_x, circle_y, circle_speed, rect_x_level2, rect_y_level2, rect_width_level2, rect_height_level2)

        # Check for collision with the gold coin
        if circle_x + circle_radius > coin_x_level2 and circle_x - circle_radius < coin_x_level2 + coin_size \
                and circle_y + circle_radius > coin_y_level2 and circle_y - circle_radius < coin_y_level2 + coin_size:
            # Transition to level 3
            current_level = 3

        # Check for collision with black lines
        if (circle_x - circle_radius <= rect_x_level2 or circle_x + circle_radius >= rect_x_level2 + rect_width_level2 or
                circle_y - circle_radius <= rect_y_level2 or circle_y + circle_radius >= rect_y_level2 + rect_height_level2):
            # Prevent movement in the collided direction
            if circle_x - circle_radius <= rect_x_level2:
                circle_x = rect_x_level2 + circle_radius
            elif circle_x + circle_radius >= rect_x_level2 + rect_width_level2:
                circle_x = rect_x_level2 + rect_width_level2 - circle_radius
            if circle_y - circle_radius <= rect_y_level2:
                circle_y = rect_y_level2 + circle_radius
            elif circle_y + circle_radius >= rect_y_level2 + rect_height_level2:
                circle_y = rect_y_level2 + rect_height_level2 - circle_radius

        # Draw the rectangle for level 2
        pygame.draw.rect(window, (255, 255, 255), (rect_x_level2, rect_y_level2, rect_width_level2, rect_height_level2))

        # Draw black lines on the perimeter of the rectangle
        pygame.draw.line(window, BLACK, (rect_x_level2, rect_y_level2), (rect_x_level2 + rect_width_level2, rect_y_level2), 3)  # Top line
        pygame.draw.line(window, BLACK, (rect_x_level2, rect_y_level2), (rect_x_level2, rect_y_level2 + rect_height_level2), 3)  # Left line
        pygame.draw.line(window, BLACK, (rect_x_level2 + rect_width_level2, rect_y_level2),
                         (rect_x_level2 + rect_width_level2, rect_y_level2 + rect_height_level2), 3)  # Right line
        pygame.draw.line(window, BLACK, (rect_x_level2, rect_y_level2 + rect_height_level2),
                         (rect_x_level2 + rect_width_level2, rect_y_level2 + rect_height_level2), 3)  # Bottom line

        # Draw the green circle
        pygame.draw.circle(window, GREEN, (circle_x, circle_y), circle_radius)

        # Draw the gold coin for level 2 as a circle
        pygame.draw.circle(window, GOLD, (coin_x_level2 + coin_size // 2, coin_y_level2 + coin_size // 2),
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
        pygame.draw.circle(window, GOLD, (coin_x_level3 + coin_size // 2, coin_y_level3 + coin_size // 2), coin_size // 2)

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
    restart_text_rect = restart_text.get_rect(center= restart_button_rect.center)
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