import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors for Day Mode
DAY_SKY = (135, 206, 235)
DAY_GROUND = (139, 69, 19)
DAY_GRASS = (34, 139, 34)

# Colors for Night Mode
NIGHT_SKY = (25, 25, 112)
NIGHT_GROUND = (64, 44, 24)
NIGHT_GRASS = (20, 60, 20)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boulder Runner")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game variables
player_x = 100
player_y = 250
player_width = 40
player_height = 60
player_velocity_y = 0
is_jumping = False
ground_level = 250

# Game state
game_state = "menu"  # menu, character_select, playing, game_over
selected_character = "human"
day_mode = True

# Gameplay variables
gravity = 1
jump_strength = -20  # Increased for higher jumps
obstacles = []
coins = []
score = 0
obstacle_speed = 5
frame_count = 0
last_obstacle_x = 0  # Track position of last boulder spawned

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)


# ===== FUNCTIONS =====

def draw_pixelated_human(x, y, is_jumping):
    """Draw a pixelated human character"""
    # Body color
    skin = (255, 220, 177)
    shirt = (100, 150, 255)
    pants = (50, 50, 100)
    
    if is_jumping:
        # Jumping pose - legs bent
        pygame.draw.rect(screen, skin, (x + 10, y + 10, 20, 20))  # Head
        pygame.draw.rect(screen, shirt, (x + 5, y + 30, 30, 20))  # Body
        pygame.draw.rect(screen, pants, (x + 5, y + 50, 12, 15))  # Leg 1
        pygame.draw.rect(screen, pants, (x + 23, y + 50, 12, 15))  # Leg 2
    else:
        # Running pose
        pygame.draw.rect(screen, skin, (x + 10, y, 20, 20))  # Head
        pygame.draw.rect(screen, shirt, (x + 5, y + 20, 30, 25))  # Body
        # Animated legs
        leg_offset = (frame_count // 5) % 8 - 4
        pygame.draw.rect(screen, pants, (x + 5, y + 45, 12, 20))  # Leg 1
        pygame.draw.rect(screen, pants, (x + 23 + leg_offset, y + 45, 12, 20))  # Leg 2


def draw_pixelated_pig(x, y, is_jumping):
    """Draw a pixelated pig character"""
    pink = (255, 182, 193)
    dark_pink = (255, 105, 180)
    
    if is_jumping:
        # Jumping pig
        pygame.draw.rect(screen, pink, (x, y + 20, 40, 30))  # Body
        pygame.draw.rect(screen, pink, (x + 30, y + 15, 15, 20))  # Head
        pygame.draw.rect(screen, dark_pink, (x + 35, y + 20, 8, 8))  # Snout
        pygame.draw.rect(screen, pink, (x + 30, y + 10, 5, 8))  # Ear 1
        pygame.draw.rect(screen, pink, (x + 40, y + 10, 5, 8))  # Ear 2
    else:
        # Running pig
        pygame.draw.rect(screen, pink, (x, y + 15, 40, 35))  # Body
        pygame.draw.rect(screen, pink, (x + 30, y + 10, 15, 25))  # Head
        pygame.draw.rect(screen, dark_pink, (x + 35, y + 20, 8, 8))  # Snout
        pygame.draw.rect(screen, pink, (x + 30, y + 5, 5, 8))  # Ear 1
        pygame.draw.rect(screen, pink, (x + 40, y + 5, 5, 8))  # Ear 2
        # Animated legs
        leg_offset = (frame_count // 5) % 6 - 3
        pygame.draw.rect(screen, pink, (x + 5, y + 50, 8, 15))  # Leg 1
        pygame.draw.rect(screen, pink, (x + 27 + leg_offset, y + 50, 8, 15))  # Leg 2


def draw_pixelated_cow(x, y, is_jumping):
    """Draw a pixelated cow character"""
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    if is_jumping:
        # Jumping cow
        pygame.draw.rect(screen, white, (x, y + 20, 45, 35))  # Body
        pygame.draw.rect(screen, black, (x + 10, y + 25, 15, 15))  # Spot 1
        pygame.draw.rect(screen, black, (x + 25, y + 40, 12, 12))  # Spot 2
        pygame.draw.rect(screen, white, (x + 35, y + 15, 18, 25))  # Head
        pygame.draw.rect(screen, black, (x + 35, y + 10, 5, 8))  # Horn 1
        pygame.draw.rect(screen, black, (x + 48, y + 10, 5, 8))  # Horn 2
    else:
        # Running cow
        pygame.draw.rect(screen, white, (x, y + 15, 45, 40))  # Body
        pygame.draw.rect(screen, black, (x + 10, y + 20, 15, 15))  # Spot 1
        pygame.draw.rect(screen, black, (x + 25, y + 35, 12, 12))  # Spot 2
        pygame.draw.rect(screen, white, (x + 35, y + 10, 18, 30))  # Head
        pygame.draw.rect(screen, black, (x + 35, y + 5, 5, 8))  # Horn 1
        pygame.draw.rect(screen, black, (x + 48, y + 5, 5, 8))  # Horn 2
        # Animated legs
        leg_offset = (frame_count // 5) % 6 - 3
        pygame.draw.rect(screen, white, (x + 5, y + 55, 10, 15))  # Leg 1
        pygame.draw.rect(screen, white, (x + 30 + leg_offset, y + 55, 10, 15))  # Leg 2


def draw_pixelated_alien(x, y, is_jumping):
    """Draw a pixelated alien character"""
    green = (0, 255, 0)
    dark_green = (0, 180, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    if is_jumping:
        # Jumping alien
        pygame.draw.rect(screen, green, (x + 5, y + 25, 35, 30))  # Body
        pygame.draw.rect(screen, green, (x + 10, y + 10, 25, 25))  # Head
        pygame.draw.rect(screen, black, (x + 13, y + 15, 8, 10))  # Eye 1
        pygame.draw.rect(screen, white, (x + 15, y + 17, 3, 4))  # Eye highlight
        pygame.draw.rect(screen, black, (x + 24, y + 15, 8, 10))  # Eye 2
        pygame.draw.rect(screen, white, (x + 26, y + 17, 3, 4))  # Eye highlight
        pygame.draw.rect(screen, dark_green, (x + 20, y + 5, 5, 8))  # Antenna
    else:
        # Running alien
        pygame.draw.rect(screen, green, (x + 5, y + 20, 35, 35))  # Body
        pygame.draw.rect(screen, green, (x + 10, y + 5, 25, 25))  # Head
        pygame.draw.rect(screen, black, (x + 13, y + 10, 8, 10))  # Eye 1
        pygame.draw.rect(screen, white, (x + 15, y + 12, 3, 4))  # Eye highlight
        pygame.draw.rect(screen, black, (x + 24, y + 10, 8, 10))  # Eye 2
        pygame.draw.rect(screen, white, (x + 26, y + 12, 3, 4))  # Eye highlight
        pygame.draw.rect(screen, dark_green, (x + 20, y, 5, 8))  # Antenna
        # Animated legs
        leg_offset = (frame_count // 5) % 6 - 3
        pygame.draw.rect(screen, green, (x + 10, y + 55, 10, 12))  # Leg 1
        pygame.draw.rect(screen, green, (x + 25 + leg_offset, y + 55, 10, 12))  # Leg 2


def draw_character(x, y, character_type, is_jumping):
    """Draw the selected character"""
    if character_type == "human":
        draw_pixelated_human(x, y, is_jumping)
    elif character_type == "pig":
        draw_pixelated_pig(x, y, is_jumping)
    elif character_type == "cow":
        draw_pixelated_cow(x, y, is_jumping)
    elif character_type == "alien":
        draw_pixelated_alien(x, y, is_jumping)


def draw_coin(x, y):
    """Draw a pixelated spinning coin"""
    gold = (255, 215, 0)
    dark_gold = (218, 165, 32)
    
    # Spinning animation based on frame count
    spin_state = (frame_count // 5) % 4
    
    if spin_state == 0 or spin_state == 2:
        # Full circle view
        pygame.draw.rect(screen, gold, (x + 5, y, 20, 30))
        pygame.draw.rect(screen, gold, (x, y + 5, 30, 20))
        pygame.draw.circle(screen, dark_gold, (x + 15, y + 15), 5)
    elif spin_state == 1:
        # Turning (thinner)
        pygame.draw.rect(screen, gold, (x + 10, y, 10, 30))
        pygame.draw.rect(screen, dark_gold, (x + 12, y + 10, 6, 10))
    else:
        # Turned (very thin)
        pygame.draw.rect(screen, gold, (x + 13, y, 4, 30))
        pygame.draw.rect(screen, dark_gold, (x + 14, y + 10, 2, 10))


def check_collision(player_x, player_y, player_width, player_height, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
    """Check if player collides with an obstacle"""
    if (player_x < obstacle_x + obstacle_width and
        player_x + player_width > obstacle_x and
        player_y < obstacle_y + obstacle_height and
        player_y + player_height > obstacle_y):
        return True
    return False


def draw_boulder(x, y):
    """Draw a textured boulder"""
    # Main boulder body
    gray = (128, 128, 128)
    dark_gray = (80, 80, 80)
    light_gray = (160, 160, 160)
    
    # Base circle (using rectangles to simulate)
    pygame.draw.rect(screen, gray, (x + 5, y, 30, 40))
    pygame.draw.rect(screen, gray, (x, y + 5, 40, 30))
    
    # Texture details
    pygame.draw.rect(screen, dark_gray, (x + 10, y + 10, 8, 8))
    pygame.draw.rect(screen, dark_gray, (x + 22, y + 20, 10, 10))
    pygame.draw.rect(screen, light_gray, (x + 8, y + 25, 6, 6))
    pygame.draw.rect(screen, light_gray, (x + 25, y + 8, 7, 7))


def draw_button(text, x, y, width, height, mouse_pos):
    """Draw a button and return True if clicked"""
    # Check if mouse is hovering
    is_hovering = (x <= mouse_pos[0] <= x + width and 
                   y <= mouse_pos[1] <= y + height)
    
    # Button color changes on hover
    if is_hovering:
        color = (100, 200, 100)
    else:
        color = (70, 170, 70)
    
    # Draw button
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 3)
    
    # Draw text
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)
    
    return is_hovering


def draw_toggle_switch(x, y, is_on, mouse_pos):
    """Draw a toggle switch for Day/Night mode"""
    switch_width = 80
    switch_height = 35
    
    # Check if mouse is hovering
    is_hovering = (x <= mouse_pos[0] <= x + switch_width and 
                   y <= mouse_pos[1] <= y + switch_height)
    
    # Switch background color
    if is_on:
        bg_color = (100, 150, 255)  # Blue for Day
    else:
        bg_color = (40, 40, 80)  # Dark for Night
    
    # Draw switch background
    pygame.draw.rect(screen, bg_color, (x, y, switch_width, switch_height), border_radius=20)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, switch_width, switch_height), 3, border_radius=20)
    
    # Draw sliding circle
    circle_x = x + 15 if not is_on else x + switch_width - 15
    circle_color = (255, 255, 255) if not is_hovering else (220, 220, 220)
    pygame.draw.circle(screen, circle_color, (circle_x, y + switch_height // 2), 12)
    pygame.draw.circle(screen, (0, 0, 0), (circle_x, y + switch_height // 2), 12, 2)
    
    return is_hovering


def draw_character_preview(character_type, x, y):
    """Draw a larger preview of character for selection screen"""
    # Scale up by drawing at different position
    draw_character(x, y - 30, character_type, False)


# ===== GAME LOOP =====
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
        
        # Keyboard controls for playing state
        if game_state == "playing":
            if event.type == pygame.KEYDOWN:
                # Jump with spacebar only
                if event.key == pygame.K_SPACE and not is_jumping:
                    is_jumping = True
                    player_velocity_y = jump_strength
    
    
    # ===== MENU STATE =====
    if game_state == "menu":
        # Draw background based on day_mode setting
        if day_mode:
            # Day background
            for i in range(5):
                shade = 135 + i * 15
                pygame.draw.rect(screen, (shade, 206, 235), (0, i * 80, SCREEN_WIDTH, 80))
            
            # Sun
            pygame.draw.circle(screen, (255, 255, 0), (700, 80), 40)
            
            # Grass with depth
            pygame.draw.rect(screen, (34, 139, 34), (0, 320, SCREEN_WIDTH, 40))
            pygame.draw.rect(screen, (25, 100, 25), (0, 360, SCREEN_WIDTH, 40))
            
            # Grass details
            for i in range(0, SCREEN_WIDTH, 25):
                pygame.draw.rect(screen, (20, 80, 20), (i, 315, 3, 12))
        else:
            # Night background
            for i in range(5):
                shade = 25 + i * 8
                pygame.draw.rect(screen, (shade, shade, 112), (0, i * 80, SCREEN_WIDTH, 80))
            
            # Moon
            pygame.draw.circle(screen, (220, 220, 220), (700, 80), 35)
            
            # Stars
            for i in range(0, SCREEN_WIDTH, 100):
                for j in range(0, 250, 80):
                    pygame.draw.rect(screen, (255, 255, 255), (i + random.randint(-10, 10), j, 2, 2))
            
            # Dark grass
            pygame.draw.rect(screen, (20, 60, 20), (0, 320, SCREEN_WIDTH, 40))
            pygame.draw.rect(screen, (15, 45, 15), (0, 360, SCREEN_WIDTH, 40))
        
        # Decorative boulders
        draw_boulder(50, 260)
        draw_boulder(650, 270)
        
        # Animated coin
        draw_coin(720, 120)
        
        # Title with shadow
        title_text = pygame.font.Font(None, 72).render("BOULDER RUNNER", True, (0, 0, 0))
        screen.blit(title_text, (152, 72))
        title_text = pygame.font.Font(None, 72).render("BOULDER RUNNER", True, (255, 215, 0))
        screen.blit(title_text, (150, 70))
        
        # Subtitle
        subtitle = small_font.render("Dodge boulders, collect coins!", True, (50, 50, 50))
        screen.blit(subtitle, (260, 140))
        
        # Day/Night Mode Toggle
        mode_label = small_font.render("Day", True, (255, 255, 255))
        screen.blit(mode_label, (300, 190))
        
        # Toggle switch
        if draw_toggle_switch(340, 183, day_mode, mouse_pos) and mouse_clicked:
            day_mode = not day_mode
        
        night_label = small_font.render("Night", True, (255, 255, 255))
        screen.blit(night_label, (430, 190))
        
        # Large Play button
        if draw_button("PLAY", 300, 240, 200, 60, mouse_pos) and mouse_clicked:
            game_state = "character_select"
        
        # Instructions at bottom with better visibility
        inst_text = small_font.render("SPACEBAR: Jump", True, (255, 255, 255))
        screen.blit(inst_text, (330, 350))
    
    
    # ===== MODE SELECT STATE (removed, now handled on menu) =====
    # elif game_state == "mode_select":
    #     ... (this section is removed)
    
    
    # ===== CHARACTER SELECT STATE =====
    elif game_state == "character_select":
        # Draw background based on mode
        if day_mode:
            screen.fill(DAY_SKY)
            pygame.draw.rect(screen, DAY_GRASS, (0, 300, SCREEN_WIDTH, 100))
        else:
            screen.fill(NIGHT_SKY)
            pygame.draw.rect(screen, NIGHT_GRASS, (0, 300, SCREEN_WIDTH, 100))
        
        # Title
        title_text = font.render("Choose Your Character", True, (255, 255, 255))
        screen.blit(title_text, (220, 30))
        
        # Character buttons with previews
        characters = ["human", "pig", "cow", "alien"]
        char_names = ["Human", "Pig", "Cow", "Alien"]
        
        for i, (char, name) in enumerate(zip(characters, char_names)):
            x_pos = 100 + i * 150
            
            # Draw preview
            draw_character_preview(char, x_pos, 150)
            
            # Draw button
            if draw_button(name, x_pos - 30, 220, 120, 40, mouse_pos) and mouse_clicked:
                selected_character = char
                game_state = "playing"
                # Reset game variables
                obstacles = []
                coins = []
                score = 0
                obstacle_speed = 5
                player_y = ground_level
                player_velocity_y = 0
                is_jumping = False
                frame_count = 0
                last_obstacle_x = 0
    
    
    # ===== PLAYING STATE =====
    elif game_state == "playing":
        # Increment frame counter
        frame_count += 1
        
        # Draw background based on mode
        if day_mode:
            screen.fill(DAY_SKY)
            # Sun
            pygame.draw.circle(screen, (255, 255, 0), (700, 80), 40)
            # Ground
            pygame.draw.rect(screen, DAY_GRASS, (0, 300, SCREEN_WIDTH, 20))
            pygame.draw.rect(screen, DAY_GROUND, (0, 320, SCREEN_WIDTH, 80))
            # Grass blades
            for i in range(0, SCREEN_WIDTH, 30):
                pygame.draw.rect(screen, (20, 100, 20), (i, 295, 3, 10))
        else:
            screen.fill(NIGHT_SKY)
            # Moon
            pygame.draw.circle(screen, (220, 220, 220), (700, 80), 35)
            # Stars
            for i in range(0, SCREEN_WIDTH, 100):
                for j in range(0, 250, 80):
                    pygame.draw.rect(screen, (255, 255, 255), (i + random.randint(-10, 10), j, 2, 2))
            # Ground
            pygame.draw.rect(screen, NIGHT_GRASS, (0, 300, SCREEN_WIDTH, 20))
            pygame.draw.rect(screen, NIGHT_GROUND, (0, 320, SCREEN_WIDTH, 80))
        
        # Apply gravity to player
        if is_jumping or player_y < ground_level:
            player_velocity_y += gravity
            player_y += player_velocity_y
            
            # Check if player landed
            if player_y >= ground_level:
                player_y = ground_level
                is_jumping = False
                player_velocity_y = 0
        
        # Adjust player hitbox
        current_height = player_height
        current_y_offset = 0
        
        # Draw player character
        draw_character(player_x, player_y, selected_character, is_jumping)
        
        # Spawn ground obstacles (boulders) with proper spacing
        # Only spawn if last boulder is far enough away (300-400 pixels)
        if len(obstacles) == 0 or obstacles[-1]['x'] < SCREEN_WIDTH - random.randint(300, 400):
            if random.randint(1, 60) == 1:
                obstacles.append({'x': SCREEN_WIDTH, 'y': 270, 'width': 40, 'height': 40})
                last_obstacle_x = SCREEN_WIDTH
        
        # Spawn coins at jump arc heights (150-200 is optimal for jump collection)
        if random.randint(1, 100) == 1:
            coin_height = random.choice([150, 165, 180, 195])
            coins.append({'x': SCREEN_WIDTH, 'y': coin_height, 'width': 30, 'height': 30})
        
        # Update and draw ground obstacles
        for obstacle in obstacles[:]:
            obstacle['x'] -= obstacle_speed
            
            # Draw boulder
            draw_boulder(obstacle['x'], obstacle['y'])
            
            # Check collision
            if check_collision(player_x, player_y + current_y_offset, player_width, current_height,
                             obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']):
                game_state = "game_over"
            
            # Remove off-screen obstacles
            if obstacle['x'] < -obstacle['width']:
                obstacles.remove(obstacle)
        
        # Update and draw coins
        for coin in coins[:]:
            coin['x'] -= obstacle_speed
            
            # Draw coin
            draw_coin(coin['x'], coin['y'])
            
            # Check if player collected the coin
            if check_collision(player_x, player_y + current_y_offset, player_width, current_height,
                             coin['x'], coin['y'], coin['width'], coin['height']):
                coins.remove(coin)
                score += 1  # Increase score when coin is collected
            
            # Remove off-screen coins
            if coin['x'] < -coin['width']:
                coins.remove(coin)
        
        # Draw HUD (score and speed)
        score_text = font.render(f"Coins: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Draw coin icon next to score
        draw_coin(130, 15)
        
        speed_text = small_font.render(f"Speed: {obstacle_speed}", True, (255, 255, 255))
        screen.blit(speed_text, (10, 50))
        
        # Draw controls hint
        controls_text = small_font.render("SPACEBAR: Jump", True, (255, 255, 255))
        screen.blit(controls_text, (SCREEN_WIDTH - 200, 10))
    
    
    # ===== GAME OVER STATE =====
    elif game_state == "game_over":
        # Draw background
        if day_mode:
            screen.fill(DAY_SKY)
            pygame.draw.rect(screen, DAY_GRASS, (0, 300, SCREEN_WIDTH, 100))
        else:
            screen.fill(NIGHT_SKY)
            pygame.draw.rect(screen, NIGHT_GRASS, (0, 300, SCREEN_WIDTH, 100))
        
        # Game over text
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, 100))
        
        # Final score with coin icon
        final_score_text = font.render(f"Coins Collected: {score}", True, (255, 255, 255))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 140, 150))
        draw_coin(SCREEN_WIDTH // 2 + 120, 155)
        
        # Character used
        char_text = small_font.render(f"Character: {selected_character.capitalize()}", True, (255, 255, 255))
        screen.blit(char_text, (SCREEN_WIDTH // 2 - 100, 200))
        
        # Buttons
        if draw_button("Play Again", 250, 250, 150, 50, mouse_pos) and mouse_clicked:
            game_state = "character_select"
        
        if draw_button("Main Menu", 410, 250, 150, 50, mouse_pos) and mouse_clicked:
            game_state = "menu"
    
    
    # Update display
    pygame.display.flip()
    
    # Control frame rate (60 FPS)
    clock.tick(60)

# Quit pygame
pygame.quit()