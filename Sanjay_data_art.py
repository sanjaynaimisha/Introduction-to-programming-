# Sanjay_data_art.py
# Main program for Dog Park Night Garden Data Visualization

"""
# AI ASSISTANCE DOCUMENTATION
  - Explaining csv.DictReader usage and file handling
   - Clarifying pygame display.flip() vs update() differences
   - Code organization review and commenting best practices
   - Understanding data normalization concepts
"""

import csv
import sys
from pathlib import Path

import pygame

from visual_objects import BoneCrystal, DogSprite

# CONFIGURATION CONSTANTS
# These define the window size and performance settings

SCREEN_WIDTH = 1280         # Window width in pixels
SCREEN_HEIGHT = 720         # Window height in pixels
FPS = 60                    # Target frames per second (60 is smooth)

# Layout constants
GRASS_HEIGHT = SCREEN_HEIGHT // 6  # Bottom grass strip height (1/6 of screen)


# DATA LOADING FUNCTIONS

def load_dog_data(path: Path):
    
    rows = []  # Empty list to store all rows
    
    # Open the file with proper encoding for special characters
    # 'newline=""' handles different line ending styles (Windows vs Mac)
    with path.open(newline="", encoding="utf-8") as f:
        # DictReader automatically uses first row as column names (keys)
        reader = csv.DictReader(f)
        
        # Loop through each row in the CSV
        for row in reader:
            rows.append(row)  # Add this row's dictionary to our list
    
    return rows


def _get_first_non_empty(row, keys):
    
    # Loop through each possible column name
    for k in keys:
        # Check if this key exists in the row dictionary
        # AND it's not None
        # AND when converted to string and whitespace removed, it's not empty
        if k in row and row[k] is not None and str(row[k]).strip() != "":
            return row[k]  # Found a good value, return it!
    
    return ""  # Didn't find any good value, return empty string


def _map_1_to_5(value_str, default=3.0):
    """
    Convert a (possibly empty) 1–5 rating into 0–1 normalized float.
    
    """
    # Try to convert string to float
    try:
        v = float(value_str)
    except (TypeError, ValueError):
        # If conversion fails (empty string, None, invalid text)
        # Use the default value instead
        v = float(default)

    # Clamp value to valid 1-5 range
    # (in case CSV has weird values like 0 or 10)
    if v < 1.0:
        v = 1.0
    if v > 5.0:
        v = 5.0
    
    # Normalize from [1, 5] range to [0, 1] range
    # Formula: (value - min) / (max - min)
    # (v - 1) / (5 - 1) = (v - 1) / 4
    return (v - 1.0) / 4.0



# BACKGROUND DRAWING FUNCTIONS

def draw_sky(surface: pygame.Surface):
    """
    Draws a night gradient background.

    """
    # Define gradient colors
    top = (10, 25, 60)       # Dark navy blue at top
    bottom = (50, 80, 140)   # Lighter blue at horizon

    # Draw one horizontal line for each pixel height
    for y in range(SCREEN_HEIGHT):
        # Calculate interpolation factor (0.0 at top, 1.0 at bottom)
        t = y / SCREEN_HEIGHT
        
        # Linearly interpolate (blend) between top and bottom colors
        # When t=0 (top), we get top color
        # When t=1 (bottom), we get bottom color
        # In between, we get a blend
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        
        # Draw this horizontal line
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))


def draw_grass(surface: pygame.Surface):
    """
    Draw single clean grass strip at bottom of screen.

    """
    color = (45, 135, 55)  # Dark green grass color
    
    # Draw rectangle at bottom of screen
    # Parameters: (x, y, width, height)
    # x=0, y=bottom-grass_height, width=full screen, height=grass_height
    pygame.draw.rect(
        surface,
        color,
        (0, SCREEN_HEIGHT - GRASS_HEIGHT, SCREEN_WIDTH, GRASS_HEIGHT),
    )


# BONE CREATION FUNCTION (DATA → VISUAL MAPPING)


def create_bones(rows):
    """
    Creates up to 20 BoneCrystal objects positioned in a 5x4 grid.

    Takes dog breed data from the CSV and converts it into visual bone crystals.

    """
    # Only use the first 20 breeds (requirement: minimum 20 rows)
    rows = rows[:20]
    bones = []  # Will store all created bones

    # Grid configuration
    cols = 5          # 5 bones per row
    row_count = 4     # 4 rows (5×4 = 20 bones)

    # Calculate horizontal spacing
    # Divide screen into (cols+1) sections to get even spacing
    spacing_x = SCREEN_WIDTH / (cols + 1)

    # Calculate vertical spacing
    top_margin = 60      # Space from top of screen
    bottom_margin = 40   # Space above grass
    
    # Calculate where grass starts
    bottom_limit = SCREEN_HEIGHT - GRASS_HEIGHT - bottom_margin
    
    # Calculate available vertical space
    vertical_space = bottom_limit - top_margin
    
    # Divide into equal rows
    spacing_y = vertical_space / (row_count + 1)

    # Create a bone for each dog breed
    for i, r in enumerate(rows):
        # Calculate grid position for this bone
        col_i = i % cols      # Column index (0-4, cycles)
        row_i = i // cols     # Row index (0-3, increases every 5)

        # Calculate actual screen coordinates
        x = (col_i + 1) * spacing_x  # Multiply by (index+1) for spacing
        y = top_margin + (row_i + 1) * spacing_y

        # === DATA EXTRACTION ===
        # Try multiple possible column names (CSV files vary!)
        
        # Energy level (how active the dog is)
        energy_raw = _get_first_non_empty(
            r,
            ["energy_level_value", "Energy Level", "energy_level"],
        )
        
        # Barking level (how vocal the dog is)
        barking_raw = _get_first_non_empty(
            r,
            ["barking_level_value", "Barking Level", "barking_level"],
        )
        
        # Shedding level (how much fur they lose)
        shedding_raw = _get_first_non_empty(
            r,
            ["shedding_level_value", "Shedding Level", "shedding_level"],
        )
        
        # Trainability (how easy to train)
        train_raw = _get_first_non_empty(
            r,
            ["trainability_level_value", "Trainability", "trainability_level"],
        )

        # === NORMALIZATION ===
        # Convert 1-5 ratings to 0.0-1.0 range for calculations
        energy = _map_1_to_5(energy_raw, default=3.0)          # Default to middle
        barking = _map_1_to_5(barking_raw, default=3.0)
        shedding = _map_1_to_5(shedding_raw, default=3.0)
        trainability = _map_1_to_5(train_raw, default=3.0)

        # === VISUAL PROPERTY CALCULATIONS ===
        
        # BONE LENGTH: More energy = longer bone
        # Range: 120-200 pixels
        length = 120 + energy * 80

        # ROTATION SPEED: Less trainable = more chaotic/faster spin
        # Stubborn dogs spin faster! Range: 0.3-1.1 radians/sec
        rotation_speed = 0.3 + (1.0 - trainability) * 0.8

        # COLOR CALCULATION: Create warm/cool color palette
        # Red channel: Higher energy = more red (warmer)
        base_r = 140 + int(80 * energy)
        
        # Green channel: Less shedding = slightly greener
        base_g = 120 + int(50 * (1.0 - shedding))
        
        # Blue channel: Quieter dogs = more blue (cooler)
        base_b = 190 + int(40 * (1.0 - barking))

        # Clamp values to valid RGB range [0, 255]
        r_col = max(0, min(255, base_r))
        g_col = max(0, min(255, base_g))
        b_col = max(0, min(255, base_b))
        color = (r_col, g_col, b_col)

        # CRYSTAL SYMMETRY: More trainable = more orderly crystals
        # Well-trained dogs have symmetric patterns
        # Range: 0.3-0.9 (30%-90% symmetry)
        symmetry = 0.3 + trainability * 0.6

        # GLOW INTENSITY: More shedding = stronger halo
        # Imagine fur creating a fuzzy glow!
        # Range: 0.4-0.9 (40%-90% brightness)
        glow_intensity = 0.4 + shedding * 0.5

        # SPARK DENSITY: Barking directly controls particle emission
        # Loud dogs = lots of sparks flying!
        # This is already 0.0-1.0 from normalization
        barking_level = barking

        # === CREATE THE BONE OBJECT ===
        # Pass all calculated visual properties to BoneCrystal constructor
        bone = BoneCrystal(
            position=(x, y),                    # Where on screen
            length=length,                      # Size
            rotation_speed=rotation_speed,      # Spin speed
            color=color,                        # RGB color
            symmetry=symmetry,                  # Crystal pattern orderliness
            glow_intensity=glow_intensity,      # Halo brightness
            barking_level=barking_level,        # Particle amount
        )
        bones.append(bone)  # Add to our list

    return bones  # Return all 20 bones


# MAIN PROGRAM

def main(csv_path: str):
    """
    1. Initializes pygame
    2. Loads dog data from CSV
    3. Creates all visual objects
    4. Runs the animation loop forever (until user quits)

    The animation loop follows the standard game loop pattern:
    - Process input (check for quit)
    - Update state (animate objects)
    - Render graphics (draw everything)
    - Display frame (show on screen)
    - Repeat at 60 FPS
    """
    # PYGAME INITIALIZATION 
    pygame.init()  # Start up pygame system
    
    # Create the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dog Park Night Garden")  # Window title

    # Create clock for framerate control
    clock = pygame.time.Clock()

    #  DATA LOADING 
    # Load dog breed data from CSV file
    data = load_dog_data(Path(csv_path))
    
    # Check if file was empty or missing
    if not data:
        print("CSV is empty or missing")
        pygame.quit()
        return

    # OBJECT CREATION
    # Create all 20 bone crystals from the data
    bones = create_bones(data)

    # Create decorative dog sprite in corner
    dog_scale = 6.5  # Make 12px sprite → 78px
    dog_height_px = int(12 * dog_scale)
    dog_x = 90  # Position from left edge
    
    # Position dog on grass (grass_top - dog_height - small_gap)
    dog_y = SCREEN_HEIGHT - GRASS_HEIGHT - dog_height_px - 5
    dog = DogSprite(dog_x, dog_y, scale=dog_scale)

    # MAIN ANIMATION LOOP
    running = True  # Loop control variable
    
    while running:
        # FRAMERATE CONTROL
        # Limit to 60 FPS and get time since last frame
        # tick(60) waits to maintain 60 FPS, returns milliseconds
        # Divide by 1000 to convert to seconds (dt = delta time)
        dt = clock.tick(FPS) / 1000.0

        # === EVENT HANDLING ===
        # Check for user inputs (quit, key presses, mouse, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User closed window
                running = False  # Exit the loop

        # UPDATE PHASE 
        # Update all animations (called every frame)
        dog.update(dt)  # Update dog tail wag animation
        
        for b in bones:
            b.update(dt)  # Update each bone (rotation, glow, particles)

        # RENDER PHASE 
        # Draw everything in correct layer order (back to front)
        
        draw_sky(screen)      # Layer 1: Sky gradient (background)
        draw_grass(screen)    # Layer 2: Grass strip

        dog.draw(screen)      # Layer 3: Dog sprite
        
        for b in bones:
            b.draw(screen)    # Layer 4: All bones (each bone draws its own layers)

        # DISPLAY 
        # Flip the display buffers (show what we just drew)
        # pygame uses double buffering: draw to back buffer,
        # then flip() swaps it to the screen instantly
        pygame.display.flip()

    # CLEANUP 
    # User quit the loop, shut down pygame properly
    pygame.quit()


# ENTRY POINT
# This special check ensures main() only runs when this file is
# executed directly (not when imported as a module)

if __name__ == "__main__":
    # Check if user provided CSV filename as command-line argument
    # Usage: python Sanjay_data_art.py my_data.csv
    if len(sys.argv) > 1:
        main(sys.argv[1])  # Use provided filename
    else:
        main("dog_data.csv")  # Default filename