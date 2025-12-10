# Dog Park Night Garden

A data visualization project that turns dog breed information into glowing bone animations.

## What This Project Does

This program reads dog breed data from a CSV file and creates a visual animation where each dog breed is shown as a glowing bone. Different characteristics of the dogs (like energy level, how much they bark, etc.) change how the bones look and move.

## The Concept

I wanted to create something that feels magical - like a nighttime garden where dog bones glow like fireflies. Each bone represents a different dog breed, and the way it looks tells you about that breed's personality.

## Data Source

I used the AKC Dog Breeds dataset which has information about 277 different dog breeds. For this project, I'm showing the first 20 breeds.

The CSV file has columns like:
- energy_level_value (how active the dog is, 1-5)
- barking_level_value (how vocal the dog is, 1-5)
- shedding_level_value (how much they shed, 1-5)
- trainability_level_value (how easy to train, 1-5)

## How Data Maps to Visuals

I decided to connect the data to visuals like this:

**Energy Level** → Controls how long the bone is and how warm the colors are
- High energy dogs = longer bones with warmer colors (reds/oranges)
- Low energy dogs = shorter bones with cooler colors

**Barking Level** → Controls how many sparkles float up from the bone
- Loud dogs = lots of particles
- Quiet dogs = fewer particles

**Shedding Level** → Controls how bright the glow around the bone is
- High shedding = brighter glow
- Low shedding = dimmer glow

**Trainability** → Controls how the crystals are arranged and rotation speed
- Easy to train = symmetric, orderly crystals and slow rotation
- Hard to train = random chaotic crystals and fast rotation

## Files in This Project

- `Sanjay_data_art.py` - The main program that runs everything
- `visual_objects.py` - Contains all the classes for the visual objects
- `dog_data.csv` - The dog breed data
- `README.md` - This file

## Technical Details

### Classes I Created

**BoneCrystal** - The main bone object that represents a dog breed
- Has a rotating bone shape
- Has crystal spikes growing from it
- Has a glowing aura around it
- Emits rising spark particles

**AuraHalo** - Creates the pulsing glow effect
- Makes the bone look like it's breathing
- Uses sine waves for smooth animation

**SparkEmitter** - Creates the floating particles
- Particles spawn at the bone and float upward
- They fade out after 1-2 seconds

**DogSprite** - A little animated dog in the corner
- Just for decoration
- Wags its tail

### Layout

The bones are arranged in a 5x4 grid (5 columns, 4 rows = 20 total).
There's a night sky gradient in the background and a grass strip at the bottom where a little dog sits.

## Problems I Solved

**Problem 1: Different CSV column names**
Sometimes the CSV might have "Energy Level" or "energy_level_value" - I wrote a helper function to check multiple possible names.

**Problem 2: Missing or invalid data**
I added error handling so if a value is missing, it uses a default (middle value of 3.0).

**Problem 3: Making smooth animations**
I used delta time (dt) to make sure animations run at the same speed regardless of framerate.

## AI Assistance

I used Claude to help me with:
- Understanding how to write good docstrings
- Learning about pygame features like SRCALPHA for transparency
- Figuring out how composition works in OOP
- Adding comments to explain my code
- 
## What I Learned

- How to read CSV files using Python's csv module
- Object-oriented programming with multiple classes
- How to use composition (objects containing other objects)
- Animation with pygame
- Converting data into visuals
- Normalizing data from one range to another

## Future Ideas

If I had more time, I might add:
- Show the dog breed name when you hover over a bone
- Let users click to see more info about that breed
- Add all 277 breeds instead of just 20
- Make the colors even more varied

