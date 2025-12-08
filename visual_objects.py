# visual_objects.py
# Visual classes for Dog Park Night Garden Data Visualization

"""
# AI ASSISTANCE DOCUMENTATION
  - Explaining pygame.Surface and SRCALPHA concepts
   - Clarifying proper use of 'self' for instance attributes
   - Code organization and commenting best practices
   - Understanding composition pattern (objects containing objects)
"""


import pygame
import math
import random


# COLOR CONSTANTS
# These define the bone's natural appearance - warm cream colors
BONE_BASE = (242, 235, 210)        # Main bone color (light cream)
BONE_SHADOW = (205, 195, 165)      # Darker shade for depth
BONE_HIGHLIGHT = (255, 250, 235)   # Lighter shade for shine



# CLASS: AuraHalo
class AuraHalo:
    """
    Creates a soft, pulsing glow behind each bone.
    
    This class handles the "breathing" halo effect that makes each bone
    look like it's glowing warmly, like a firefly or ember.
    
    Attributes:
        position (list): [x, y] coordinates where the glow is centered
        base_radius (float): Starting size of the glow in pixels
        intensity (float): How bright the glow is (0.0 to 1.0)
        color (tuple): RGB color of the glow (r, g, b)
        pulse_speed (float): How fast the glow breathes in/out
        time (float): Tracks animation time for pulsing effect
    """
    
    def __init__(self, position, base_radius, intensity, color, pulse_speed):
        """
        Initialize the glowing halo.
        
        Args:
            position: [x, y] where to draw the glow
            base_radius: Base size in pixels
            intensity: Brightness (0.0-1.0)
            color: RGB tuple like (255, 200, 100)
            pulse_speed: Animation speed multiplier
        """
        self.position = list(position)      # Copy position so we can modify it
        self.base_radius = base_radius      # Store base size
        self.intensity = intensity          # Store brightness
        self.color = color                  # Store color
        self.pulse_speed = pulse_speed      # Store animation speed
        self.time = 0.0                     # Animation timer starts at 0

    def update(self, dt):
        """
        Update the animation timer.
        Called every frame to advance the pulsing animation.
        """
        self.time += dt  # Add time to make pulse animation progress

    def draw(self, surface):
        """
        Draw the pulsing glow on screen.
        Creates a "breathing" effect using sine waves and draws
        3 layers of circles with transparency for a soft look.
        """
        # Get integer coordinates for drawing
        x = int(self.position[0])
        y = int(self.position[1])

        # Calculate pulsing size using sine wave
        # sin() gives values between -1 and 1
        # We multiply by 0.3 to get -0.3 to 0.3
        # Then add 1.0 to get range of 0.7 to 1.3
        # This makes the glow shrink/grow smoothly
        pulse = math.sin(self.time * self.pulse_speed) * 0.3 + 1.0
        radius = int(self.base_radius * pulse)

        # Draw 3 concentric circles for smooth gradient effect
        for i in range(3):
            # Each layer is smaller than the last
            r = max(1, radius - i * 8)  # Subtract 8 pixels per layer
            
            # Each layer is more transparent than the last
            alpha = max(40, int(140 * self.intensity) - i * 30)

            # Create a temporary surface with transparency support
            # SRCALPHA means this surface can have transparent pixels
            glow = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            
            # Draw a circle on the temporary surface
            # The * unpacks the RGB tuple, and we add alpha for transparency
            pygame.draw.circle(glow, (*self.color, alpha), (r, r), r)
            
            # Draw (blit) the glow onto the main screen
            # Centered at (x, y) by offsetting by radius
            surface.blit(glow, (x - r, y - r))



# CLASS: SparkEmitter
class SparkEmitter:
    """
    Creates small glowing particles that float upward.
    
    This particle system emits tiny dots that rise slowly, creating
    the effect of warm embers or heat rising from the bones.
    
    Attributes:
        origin (list): [x, y] where particles spawn
        max_particles (int): Maximum number of particles at once
        spawn_rate (float): How many particles per second
        color (tuple): RGB color for the particles
        speed (float): How fast particles move upward (pixels/second)
        particles (list): List of active particles (each is a list of data)
        timer (float): Tracks when to spawn next particle
    """
    
    def __init__(self, origin, max_particles, spawn_rate, color, speed):
        """
        Initialize the particle emitter.
        Args:
            origin: [x, y] spawn point
            max_particles: Max particles allowed at once
            spawn_rate: Particles spawned per second
            color: RGB tuple
            speed: Upward speed in pixels/second
        """
        self.origin = list(origin)              # Where particles spawn
        self.max_particles = max_particles      # Limit on particle count
        self.spawn_rate = spawn_rate            # Emission frequency
        self.color = color                      # Particle color
        self.speed = speed                      # Movement speed

        self.particles = []  # List to hold all active particles
        self.timer = 0.0     # Timer to control spawning

    def update(self, dt):
        """
        Update all particles - spawn new ones and move existing ones.

        """
        self.timer += dt  # Advance spawn timer
        
        # Calculate time between spawns
        # If spawn_rate is 5, interval is 0.2 seconds
        interval = 1.0 / self.spawn_rate

        # Spawn particles when timer is ready
        while self.timer >= interval and len(self.particles) < self.max_particles:
            self.timer -= interval  # Reset timer for next spawn
            x, y = self.origin      # Get spawn position
            
            # Create new particle as a list:
            # [x, y, vertical_velocity, age, lifetime]
            self.particles.append([
                x + random.uniform(-4, 4),      # Random X offset (slight spread)
                y + random.uniform(-4, 4),      # Random Y offset
                -self.speed * random.uniform(0.8, 1.2),  # Upward speed (negative Y)
                0.0,                            # Age starts at 0
                random.uniform(1.0, 2.0),       # Lives 1-2 seconds
            ])

        # Update all existing particles
        for p in self.particles:
            p[1] += p[2] * dt  # Move Y position (index 1) by velocity (index 2)
            p[3] += dt         # Increase age (index 3)

        # Remove dead particles (age >= lifetime)
        # List comprehension: keep only particles where age < lifetime
        self.particles = [p for p in self.particles if p[3] < p[4]]

    def draw(self, surface):
        """
        Draw all active particles as small circles.
    
        """
        for p in self.particles:
            # Draw each particle as a small circle (radius 2)
            # p[0] is X, p[1] is Y
            pygame.draw.circle(surface, self.color, (int(p[0]), int(p[1])), 2)



# CLASS: BoneCrystal
class BoneCrystal:
    """
    Main visual element: A glowing bone with crystal shards and sparks.
    
    Each BoneCrystal represents one dog breed
    from the CSV data. It combines:
    - A rotating cartoon bone shape
    - Crystal spikes growing from the bone
    - A pulsing glow (AuraHalo)
    - Rising spark particles (SparkEmitter)
    
    This demonstrates COMPOSITION - BoneCrystal contains other objects!
    
        position (list): [x, y] center position
        length (float): How long the bone is in pixels
        rotation_speed (float): How fast it spins (radians/second)
        color (tuple): RGB color for glow and crystals
        symmetry (float): 0.0-1.0, how orderly the crystals are
        glow_intensity (float): 0.0-1.0, how bright the glow is
        angle (float): Current rotation angle in radians
        aura (AuraHalo): The glow object (composition!)
        sparks (SparkEmitter): The particle system (composition!)
        shards (list): Data for crystal spikes
    """
    
    def __init__(self, position, length, rotation_speed, color, symmetry, glow_intensity, barking_level):
        """
        Initialize a bone crystal.

            position: [x, y] where to draw it
            length: Bone length in pixels
            rotation_speed: Spin speed in radians/second
            color: RGB tuple for glow/crystals
            symmetry: 0.0-1.0, crystal orderliness
            glow_intensity: 0.0-1.0, glow brightness
            barking_level: 0.0-1.0, controls spark amount
        """
        # Store basic properties
        self.position = list(position)          # Center position
        self.length = length                    # Bone size
        self.rotation_speed = rotation_speed    # Spin speed
        self.color = color                      # Color scheme
        self.symmetry = symmetry                # Crystal pattern
        self.glow_intensity = glow_intensity    # Glow brightness
        self.angle = 0.0                        # Current rotation (starts at 0)

        # COMPOSITION EXAMPLE 1: Create a glow halo object
        # BoneCrystal "has a" AuraHalo
        self.aura = AuraHalo(
            position=position,
            base_radius=length * 0.35,      # Glow size based on bone size
            intensity=glow_intensity,
            color=color,
            pulse_speed=0.8,
        )

        # COMPOSITION EXAMPLE 2: Create a particle emitter
        # BoneCrystal "has a" SparkEmitter
        self.sparks = SparkEmitter(
            origin=position,
            max_particles=10 + int(barking_level * 40),  # More barking = more particles
            spawn_rate=4 + barking_level * 15,           # Barking affects spawn rate
            color=color,
            speed=20 + barking_level * 50,               # Barking affects speed
        )

        self.shards = []        # Will hold crystal spike data
        self._make_shards()     # Generate the crystals

    def _make_shards(self):
        """
        Generate crystal spike positions.
        
        Creates random crystal shards that grow from the bone.
        High symmetry = mirrored spikes on both sides
        Low symmetry = random chaotic placement
        
        This is a private helper method (starts with _)
        """
        self.shards.clear()  # Clear any existing shards
        
        # Create 5 groups of crystals
        for _ in range(5):
            # Random position along the bone (-30% to +30% of length)
            offset = random.uniform(-0.3, 0.3) * self.length
            
            # Random spike size
            size = random.uniform(10, 18)

            # Check symmetry to decide placement
            if random.random() < self.symmetry:
                # High symmetry: add matching spikes on both sides
                self.shards.append((offset, 1, size))   # Right side (1)
                self.shards.append((offset, -1, size))  # Left side (-1)
            else:
                # Low symmetry: add spike on random side only
                self.shards.append((offset, random.choice([-1, 1]), size))

    def update(self, dt):
        """
        Update animation - called every frame.
        
        Rotates the bone and updates all sub-components.
        
        """
        self.angle += self.rotation_speed * dt  # Rotate the bone
        self.aura.update(dt)                    # Update glow animation
        self.sparks.update(dt)                  # Update particles

    def draw(self, surface):
    
        self.aura.draw(surface)         # Layer 1: Background glow
        self._draw_bone(surface)        # Layer 2: Bone shape
        self._draw_shards(surface)      # Layer 3: Crystal spikes
        self.sparks.draw(surface)       # Layer 4: Particles

    def _draw_bone(self, surface):
        """
        Draw the cartoon bone shape with shading.
        
        Creates a classic dog bone:
        - Center shaft (long part)
        - Rounded ends (knobs)
        - Small lobes on each end
        - Shadow and highlight lines for depth

        """
        cx, cy = self.position  # Center position
        a = self.angle          # Current rotation angle

        # Calculate direction vectors using trigonometry
        # dx, dy = direction along the bone
        dx = math.cos(a)
        dy = math.sin(a)
        
        # nx, ny = direction perpendicular to bone (for width)
        nx = -dy
        ny = dx

        # Calculate bone endpoints
        half = self.length / 2
        sx = cx - dx * half  # Start X
        sy = cy - dy * half  # Start Y
        ex = cx + dx * half  # End X
        ey = cy + dy * half  # End Y

        # Calculate bone dimensions
        shaft_w = int(8 + self.length * 0.06)  # Center shaft width
        end_r = int(self.length * 0.22)         # End circle radius

        # Draw the center shaft (long part of bone)
        pygame.draw.line(surface, BONE_BASE, (sx, sy), (ex, ey), shaft_w)

        # Draw main circles at each end
        pygame.draw.circle(surface, BONE_BASE, (int(sx), int(sy)), end_r)
        pygame.draw.circle(surface, BONE_BASE, (int(ex), int(ey)), end_r)

        # Add small lobes to create classic bone shape
        lobe = end_r * 0.7  # Lobe offset distance
        
        for s in (-1, 1):  # Loop for both sides (left and right)
            # Start end lobes
            pygame.draw.circle(surface, BONE_BASE,
                (int(sx + nx * lobe * s), int(sy + ny * lobe * s)),
                int(end_r * 0.75)
            )
            # End end lobes
            pygame.draw.circle(surface, BONE_BASE,
                (int(ex + nx * lobe * s), int(ey + ny * lobe * s)),
                int(end_r * 0.75)
            )

        # Add shadow line (bottom edge for depth)
        shadow_off = shaft_w * 0.3  # Shadow offset
        pygame.draw.line(
            surface, BONE_SHADOW,
            (sx + nx * shadow_off, sy + ny * shadow_off),
            (ex + nx * shadow_off, ey + ny * shadow_off),
            max(2, shaft_w // 4)  # Shadow line thickness
        )

        # Add highlight line (top edge for shine)
        pygame.draw.line(
            surface, BONE_HIGHLIGHT,
            (sx - nx * shadow_off, sy - ny * shadow_off),
            (ex - nx * shadow_off, ey - ny * shadow_off),
            max(1, shaft_w // 5)  # Highlight line thickness
        )

    def _draw_shards(self, surface):
        """
        Draw the crystal spikes growing from the bone.
        
        Each shard is a line extending outward from the bone surface.
        They rotate with the bone!
        
        """
        cx, cy = self.position  # Center position
        a = self.angle          # Current rotation

        # Calculate direction vectors (same as bone drawing)
        dx = math.cos(a)
        dy = math.sin(a)
        nx = -dy
        ny = dx

        # Make crystals slightly brighter than base color
        r, g, b = self.color
        shard_color = (min(255, r+25), min(255, g+25), min(255, b+25))

        # Draw each crystal spike
        for off, side, size in self.shards:
            # Calculate base point on bone surface
            # off = position along bone
            # side = which side (-1 or 1)
            bx = cx + dx * off + nx * side * 12
            by = cy + dy * off + ny * side * 12

            # Calculate tip point extending outward
            tx = bx + nx * side * size
            ty = by + ny * side * size

            # Draw the spike as a thick line
            pygame.draw.line(surface, shard_color, (bx, by), (tx, ty), 3)



# CLASS: DogSprite
class DogSprite:
    """
    A cute pixel-art dog that wags its tail.
    
    This is a decorative element that adds charm to the scene.
    It's just a simple animation, not connected to the CSV data.
    
    Attributes:
        x (int): X position on screen
        y (int): Y position on screen
        scale (float): Size multiplier (makes 12px sprite bigger)
        frame (int): Current animation frame (0-3)
        time (float): Animation timer
        frames (list): Pre-drawn animation frames
    """
    
    def __init__(self, x, y, scale=6.5):
        """
        Initialize the dog sprite.
        
        """
        self.x = x              # Position
        self.y = y
        self.scale = scale      # Size
        self.frame = 0          # Start at frame 0
        self.time = 0.0         # Animation timer
        self.frames = self._make_frames()  # Generate all frames

    def _make_frames(self):
        """
        Create all 4 animation frames.
        
        Draws a simple pixel-art dog with different tail positions.
        This is pure pixel art - drawing rectangles to make a dog shape!
        
        Returns:
            list: 4 pygame.Surface objects (the frames)
        """
        frames = []  # Will hold all frames
        
        # Create 4 frames for tail wag animation
        for i in range(4):
            # Create a small 12x12 pixel canvas
            # SRCALPHA allows transparent background
            surf = pygame.Surface((12, 12), pygame.SRCALPHA)

            # Define color palette
            body = (240, 225, 200)      # Light tan
            shadow = (200, 185, 150)    # Dark tan
            ear = (180, 135, 110)       # Brown
            nose = (60, 50, 50)         # Dark nose

            # Draw body rectangle
            pygame.draw.rect(surf, body, (3, 6, 6, 4))
            pygame.draw.rect(surf, shadow, (3, 9, 6, 1))  # Body shadow

            # Head position changes slightly in frames 0 and 2 (bob effect)
            head_y = 3 if i in (0, 2) else 4
            
            # Draw head
            pygame.draw.rect(surf, body, (1, head_y, 5, 4))
            pygame.draw.rect(surf, shadow, (1, head_y + 3, 5, 1))  # Head shadow

            # Draw ear
            pygame.draw.rect(surf, ear, (1, head_y - 1, 2, 2))
            
            # Draw nose
            pygame.draw.rect(surf, nose, (5, head_y + 2, 1, 1))

            # Draw legs
            pygame.draw.rect(surf, shadow, (3, 10, 2, 2))  # Left leg
            pygame.draw.rect(surf, shadow, (7, 10, 2, 2))  # Right leg

            # Draw tail in different positions (this creates the wag!)
            if i == 0:
                pygame.draw.rect(surf, body, (9, 5, 2, 2))    # Middle
            elif i == 1:
                pygame.draw.rect(surf, body, (9, 4, 2, 2))    # Up
            elif i == 2:
                pygame.draw.rect(surf, body, (9, 3, 2, 2))    # Higher
            else:
                pygame.draw.rect(surf, body, (9, 4, 2, 2))    # Back to up

            frames.append(surf)  # Add this frame to the list
            
        return frames

    def update(self, dt):
        """
        Update animation timer and advance frames.
        
        """
        self.time += dt  # Add time
        
        # Every 0.18 seconds (180ms), advance to next frame
        if self.time > 0.18:
            self.time = 0  # Reset timer
            # Advance frame, loop back to 0 after frame 3
            self.frame = (self.frame + 1) % len(self.frames)

    def draw(self, surface):
        """
        Draw the current animation frame.
        
        """
        img = self.frames[self.frame]  # Get current frame
        size = int(12 * self.scale)     # Calculate scaled size
        
        # Scale the 12x12 image up to the larger size
        img = pygame.transform.scale(img, (size, size))
        
        # Draw it at the dog's position
        surface.blit(img, (self.x, self.y))