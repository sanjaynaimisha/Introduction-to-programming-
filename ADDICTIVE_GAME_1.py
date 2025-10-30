# Import the pygame library
import pygame

# Initialize pygame - this must be done before using pygame features
pygame.init()

# Set up the game window dimensions
WIDTH = 800
HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("Runner Game")

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Set up font for displaying text
# Parameters: font name (None = default), font size
font = pygame.font.Font(None, 48)

# Define colors using RGB values (Red, Green, Blue)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GRAY = (128, 128, 128)
DARK_GRAY = (80, 80, 80)
RED = (255, 0, 0)

# Player properties - position, size, and physics
player_x = 100  # Fixed X position - player stays on left side
player_y = 450  # Starting Y position
player_width = 50
player_height = 50
player_velocity_y = 0  # Current vertical speed (negative = moving up, positive = moving down)

# Physics constants
gravity = 0.8  # How fast the player accelerates downward
jump_strength = -15  # How much upward velocity jumping gives (negative = up)
ground_level = HEIGHT - player_height - 50  # Where the ground is located

# Obstacle properties - position, size, and speed
obstacle_x = 800  # Start off-screen to the right
obstacle_y = ground_level
obstacle_width = 50  # Width for collision detection
obstacle_height = 50  # Height for collision detection
obstacle_speed = 6  # How fast obstacles move left
obstacle_radius = 25  # Radius of the boulder circle

# Game state variables
running = True
game_over = False
score = 0  # Tracks player's score

# Main game loop - runs until the player quits
while running:
    # Event handling - check for all events that happened this frame
    for event in pygame.event.get():
        # Check if the user clicked the X button to close the window
        if event.type == pygame.QUIT:
            running = False
        
        # Check for key press events (single press, not held down)
        if event.type == pygame.KEYDOWN:
            # Jump when spacebar is pressed and player is on the ground
            if event.key == pygame.K_SPACE and player_y >= ground_level and not game_over:
                player_velocity_y = jump_strength
    
    # Only update game if not game over
    if not game_over:
        # Apply gravity to the player's vertical velocity
        player_velocity_y += gravity
        
        # Update player's Y position based on velocity
        player_y += player_velocity_y
        
        # Check if player has landed on the ground
        if player_y >= ground_level:
            player_y = ground_level  # Set position exactly at ground level
            player_velocity_y = 0  # Stop downward movement
        
        # Move obstacle to the left
        obstacle_x -= obstacle_speed
        
        # Check if obstacle has gone off the left side of the screen
        if obstacle_x < -obstacle_width:
            # Reset obstacle to the right side of the screen
            obstacle_x = WIDTH
            # Increase score when player successfully passes an obstacle
            score += 1
        
        # Collision detection - check if player rectangle overlaps with obstacle rectangle
        # Check if rectangles overlap on X axis
        x_overlap = (player_x < obstacle_x + obstacle_width and 
                     player_x + player_width > obstacle_x)
        
        # Check if rectangles overlap on Y axis
        y_overlap = (player_y < obstacle_y + obstacle_height and 
                     player_y + player_height > obstacle_y)
        
        # If both X and Y overlap, there is a collision
        if x_overlap and y_overlap:
            game_over = True
    
    # Fill the screen with background color (black)
    screen.fill(BLACK)
    
    # Draw a ground line (optional visual reference)
    pygame.draw.line(screen, WHITE, (0, ground_level + player_height), (WIDTH, ground_level + player_height), 2)
    
    # Draw the stick figure player
    # Calculate center position for the stick figure based on player collision box
    stick_center_x = player_x + player_width // 2
    stick_bottom_y = player_y + player_height
    
    # Choose color based on game state
    if game_over:
        stick_color = RED
    else:
        stick_color = WHITE
    
    # Draw head - circle at top
    head_y = stick_bottom_y - 45
    pygame.draw.circle(screen, stick_color, (stick_center_x, head_y), 8)
    
    # Draw body - vertical line from head to hips
    body_top_y = head_y + 8
    body_bottom_y = stick_bottom_y - 15
    pygame.draw.line(screen, stick_color, (stick_center_x, body_top_y), (stick_center_x, body_bottom_y), 3)
    
    # Draw arms - two diagonal lines from upper body
    arm_y = body_top_y + 5
    # Left arm
    pygame.draw.line(screen, stick_color, (stick_center_x, arm_y), (stick_center_x - 12, arm_y + 10), 3)
    # Right arm
    pygame.draw.line(screen, stick_color, (stick_center_x, arm_y), (stick_center_x + 12, arm_y + 10), 3)
    
    # Draw legs - two lines from bottom of body to ground
    # Left leg
    pygame.draw.line(screen, stick_color, (stick_center_x, body_bottom_y), (stick_center_x - 10, stick_bottom_y), 3)
    # Right leg
    pygame.draw.line(screen, stick_color, (stick_center_x, body_bottom_y), (stick_center_x + 10, stick_bottom_y), 3)
    
    # Draw the boulder obstacle
    # Calculate center of the boulder based on obstacle position
    boulder_center_x = obstacle_x + obstacle_width // 2
    boulder_center_y = obstacle_y + obstacle_height // 2
    
    # Draw outer circle (darker gray for shadow effect)
    pygame.draw.circle(screen, DARK_GRAY, (boulder_center_x + 2, boulder_center_y + 2), obstacle_radius)
    # Draw main boulder circle
    pygame.draw.circle(screen, GRAY, (boulder_center_x, boulder_center_y), obstacle_radius)
    
    # Create text surface with the score
    # Convert score number to string for display
    score_text = font.render("Score: " + str(score), True, WHITE)
    
    # Draw the score in the top-left corner
    # Parameters: surface to draw, position (x, y)
    screen.blit(score_text, (10, 10))
    
    # If game is over, display game over message
    if game_over:
        game_over_text = font.render("GAME OVER", True, RED)
        # Center the text on screen
        # Get the width of the text to calculate center position
        text_width = game_over_text.get_width()
        screen.blit(game_over_text, (WIDTH // 2 - text_width // 2, HEIGHT // 2))
    
    # Update the display to show everything we drew
    pygame.display.flip()
    
    # Control the frame rate - run at 60 frames per second
    clock.tick(60)

# Quit pygame properly when the loop ends
pygame.quit()
