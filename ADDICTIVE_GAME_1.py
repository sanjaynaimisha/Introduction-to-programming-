# Import the pygame library
import pygame
import random

# Initialize pygame - this must be done before using pygame features
pygame.init()

# Set up the game window dimensions
WIDTH = 800
HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("Stick Dash")

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Set up fonts for displaying text
# Large font for title and game over
font_large = pygame.font.Font(None, 48)
# Medium font for instructions
font_medium = pygame.font.Font(None, 32)
# Small font for detailed instructions
font_small = pygame.font.Font(None, 24)

# Define colors using RGB values (Red, Green, Blue)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
GRAY = (128, 128, 128)
DARK_GRAY = (80, 80, 80)
LIGHT_GRAY = (160, 160, 160)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)

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

# Base obstacle speed - will increase as score increases
base_obstacle_speed = 6
obstacle_speed = base_obstacle_speed

# Create a list to store multiple obstacles
# Each obstacle is a list: [x_position, y_position, width, height, radius]
obstacles = []

# Add initial obstacles with random spacing
obstacles.append([800, ground_level, 50, 50, 25])
obstacles.append([1100, ground_level, 60, 60, 30])
obstacles.append([1450, ground_level, 45, 45, 22])

# Game state variables
running = True
game_over = False
score = 0  # Tracks player's score
frame_count = 0  # Counts frames for animation
start_time = pygame.time.get_ticks()  # Track game start time for timer

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
        # Increment frame counter for animations
        frame_count += 1
        
        # Apply gravity to the player's vertical velocity
        player_velocity_y += gravity
        
        # Update player's Y position based on velocity
        player_y += player_velocity_y
        
        # Check if player has landed on the ground
        if player_y >= ground_level:
            player_y = ground_level  # Set position exactly at ground level
            player_velocity_y = 0  # Stop downward movement
        
        # Increase obstacle speed based on score (difficulty increases)
        # Every 5 points, increase speed by 0.5
        obstacle_speed = base_obstacle_speed + (score // 5) * 0.5
        
        # Update all obstacles in the list
        for obstacle in obstacles:
            # Move obstacle to the left
            obstacle[0] -= obstacle_speed
            
            # Check if obstacle has gone off the left side of the screen
            if obstacle[0] < -obstacle[2]:
                # Reset obstacle to the right side with random spacing
                obstacle[0] = WIDTH + random.randint(200, 500)
                # Randomly vary obstacle size
                size = random.choice([45, 50, 60])
                obstacle[2] = size  # width
                obstacle[3] = size  # height
                obstacle[4] = size // 2  # radius
                # Increase score when player successfully passes an obstacle
                score += 1
            
            # Collision detection - check if player overlaps with this obstacle
            # Check if rectangles overlap on X axis
            x_overlap = (player_x < obstacle[0] + obstacle[2] and 
                         player_x + player_width > obstacle[0])
            
            # Check if rectangles overlap on Y axis
            y_overlap = (player_y < obstacle[1] + obstacle[3] and 
                         player_y + player_height > obstacle[1])
            
            # If both X and Y overlap, there is a collision
            if x_overlap and y_overlap:
                game_over = True
    
    # Calculate elapsed time in seconds
    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    
    # Fill the screen with sky blue background
    screen.fill(SKY_BLUE)
    
    # Draw ground (brown rectangle at bottom)
    pygame.draw.rect(screen, BROWN, (0, ground_level + player_height, WIDTH, HEIGHT))
    
    # Draw grass on top of ground (green line with small rectangles)
    pygame.draw.line(screen, GREEN, (0, ground_level + player_height), (WIDTH, ground_level + player_height), 4)
    # Draw small grass blades
    for grass_x in range(0, WIDTH, 30):
        pygame.draw.line(screen, GREEN, (grass_x, ground_level + player_height), 
                        (grass_x, ground_level + player_height - 8), 2)
    
    # ========== DRAW INSTRUCTIONS SECTION ==========
    # Draw semi-transparent background for instructions
    instruction_bg = pygame.Surface((WIDTH, 155))
    instruction_bg.set_alpha(180)
    instruction_bg.fill(BLACK)
    screen.blit(instruction_bg, (0, 0))
    
    # Draw game title at the top
    title_text = font_large.render("BOULDER RUNNER", True, YELLOW)
    title_width = title_text.get_width()
    screen.blit(title_text, (WIDTH // 2 - title_width // 2, 10))
    
    # Draw controls instruction
    controls_text = font_small.render("Controls: Press SPACEBAR to Jump", True, WHITE)
    screen.blit(controls_text, (20, 70))
    
    # Draw goal instruction
    goal_text = font_small.render("Goal: Avoid the boulders!", True, WHITE)
    screen.blit(goal_text, (20, 95))
    
    # Draw how to win/stay alive instruction
    survive_text = font_small.render("Stay Alive: Jump over boulders - Speed increases every 5 points!", True, WHITE)
    screen.blit(survive_text, (20, 120))
    
    # Draw a separator line between instructions and game area
    pygame.draw.line(screen, WHITE, (0, 155), (WIDTH, 155), 2)
    # ========== END INSTRUCTIONS SECTION ==========
    
    # Draw the animated stick figure player
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
    
    # Draw arms - two diagonal lines from upper body with pumping motion
    arm_y = body_top_y + 5
    # Animate arms based on frame count (pumping motion when running)
    if player_y >= ground_level:  # Only animate when on ground
        arm_offset = 3 if (frame_count // 10) % 2 == 0 else -3
    else:
        arm_offset = 0
    # Left arm
    pygame.draw.line(screen, stick_color, (stick_center_x, arm_y), (stick_center_x - 12, arm_y + 10 + arm_offset), 3)
    # Right arm
    pygame.draw.line(screen, stick_color, (stick_center_x, arm_y), (stick_center_x + 12, arm_y + 10 - arm_offset), 3)
    
    # Draw legs - animated running motion when on ground
    if player_y >= ground_level:  # Running animation
        # Alternate leg positions to simulate running
        if (frame_count // 8) % 2 == 0:
            # Left leg forward, right leg back
            pygame.draw.line(screen, stick_color, (stick_center_x, body_bottom_y), (stick_center_x - 8, stick_bottom_y), 3)
            pygame.draw.line(screen, stick_color, (stick_center_x, body_bottom_y), (stick_center_x + 12, stick_bottom_y), 3)
        else:
            # Right leg forward, left leg back
            pygame.draw.line(screen, stick_color, (stick_center_x, body_bottom_y), (stick_center_x - 12, stick_bottom_y), 3)
            pygame.draw.line(screen, stick_color, (stick_center_x, body_bottom_y), (stick_center_x + 8, stick_bottom_y), 3)
    else:  # Jumping - legs together
        pygame.draw.line(screen, stick_color, (stick_center_x, body_bottom_y), (stick_center_x - 6, stick_bottom_y), 3)
        pygame.draw.line(screen, stick_color, (stick_center_x, body_bottom_y), (stick_center_x + 6, stick_bottom_y), 3)
    
    # Draw all boulder obstacles with enhanced graphics
    for obstacle in obstacles:
        # Calculate center of the boulder
        boulder_center_x = obstacle[0] + obstacle[2] // 2
        boulder_center_y = obstacle[1] + obstacle[3] // 2
        boulder_radius = obstacle[4]
        
        # Draw shadow (darker gray circle offset down and right)
        pygame.draw.circle(screen, DARK_GRAY, (boulder_center_x + 3, boulder_center_y + 3), boulder_radius)
        
        # Draw main boulder circle
        pygame.draw.circle(screen, GRAY, (boulder_center_x, boulder_center_y), boulder_radius)
        
        # Add texture details to boulder (small circles for rock texture)
        # Light spot (top-left for highlight)
        pygame.draw.circle(screen, LIGHT_GRAY, (boulder_center_x - boulder_radius // 3, boulder_center_y - boulder_radius // 3), boulder_radius // 5)
        
        # Dark spots (cracks/details)
        pygame.draw.circle(screen, DARK_GRAY, (boulder_center_x + boulder_radius // 4, boulder_center_y), boulder_radius // 6)
        pygame.draw.circle(screen, DARK_GRAY, (boulder_center_x - boulder_radius // 6, boulder_center_y + boulder_radius // 4), boulder_radius // 7)
        pygame.draw.circle(screen, DARK_GRAY, (boulder_center_x + boulder_radius // 3, boulder_center_y + boulder_radius // 3), boulder_radius // 8)
    
    # Create text surface with the score
    score_text = font_medium.render("Score: " + str(score), True, WHITE)
    # Draw score in top right corner
    score_width = score_text.get_width()
    screen.blit(score_text, (WIDTH - score_width - 20, 15))
    
    # Display timer below score
    if not game_over:
        timer_text = font_small.render("Time: " + str(elapsed_time) + "s", True, WHITE)
        timer_width = timer_text.get_width()
        screen.blit(timer_text, (WIDTH - timer_width - 20, 55))
    
    # Display current speed
    speed_text = font_small.render("Speed: " + str(round(obstacle_speed, 1)), True, YELLOW)
    speed_width = speed_text.get_width()
    screen.blit(speed_text, (WIDTH - speed_width - 20, 85))
    
    # If game is over, display game over message
    if game_over:
        # Semi-transparent black background for game over screen
        game_over_bg = pygame.Surface
        # If game is over, display game over message
    if game_over:
        # Semi-transparent black background for game over screen
        game_over_bg = pygame.Surface((WIDTH, HEIGHT))
        game_over_bg.set_alpha(150)
        game_over_bg.fill(BLACK)
        screen.blit(game_over_bg, (0, 0))
        
        # Game over text
        game_over_text = font_large.render("GAME OVER", True, RED)
        text_width = game_over_text.get_width()
        screen.blit(game_over_text, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 60))
        
        # Display final score
        final_score_text = font_medium.render("Final Score: " + str(score), True, WHITE)
        final_score_width = final_score_text.get_width()
        screen.blit(final_score_text, (WIDTH // 2 - final_score_width // 2, HEIGHT // 2))
        
        # Display survival time
        time_text = font_medium.render("Survived: " + str(elapsed_time) + " seconds", True, WHITE)
        time_width = time_text.get_width()
        screen.blit(time_text, (WIDTH // 2 - time_width // 2, HEIGHT // 2 + 40))
    
    # Update the display to show everything we drew
    pygame.display.flip()
    
    # Control the frame rate - run at 60 frames per second
    clock.tick(60)

# Quit pygame properly when the loop ends
pygame.quit()
