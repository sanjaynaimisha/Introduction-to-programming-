# THE CURSED LIBRARY
# Choose Your Own Adventure Game
# Description: A student discovers a mysterious ancient library that appears 
#              only at midnight. Solve puzzles and make choices to escape 
#              before sunrise or be trapped forever.

# --- Imports ---
import time

# --- Constants ---
PAUSE_TIME = 1
MAX_CANDLES = 5

# --- Global Variables ---
candles_remaining = MAX_CANDLES
player_choices = []
has_key = False

# --- Helper Functions ---

def pause():
    """Adds dramatic pause between story elements for pacing"""
    time.sleep(PAUSE_TIME)

def show_candles():
    """Display remaining candle light as a visual indicator"""
    print("\nCandles remaining: ", end="")
    for i in range(candles_remaining):
        print("🕯️ ", end="")
    for i in range(MAX_CANDLES - candles_remaining):
        print("💨 ", end="")
    print(f" ({candles_remaining} left)\n")

def extinguish_candle():
    """Reduce candle count by one"""
    global candles_remaining
    candles_remaining -= 1
    if candles_remaining <= 0:
        game_over("The last candle flickers out. Darkness consumes you, and you are lost forever in the library.")

def mysterious_whisper():
    """Display a mysterious whispering animation"""
    whisper_stages = ["The books whisper", "The books whisper.", "The books whisper..", "The books whisper..."]
    for stage in whisper_stages:
        print(stage, end='\r')
        time.sleep(0.4)
    print("The books whisper... 'Choose wisely'")

def time_passes():
    """Show time passage with a ticking animation"""
    print("\nTime passes", end="")
    for i in range(3):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print(" ⏰")

# --- Game Logic Functions ---

def game_over(reason):
    """Handle all losing scenarios and end the game"""
    print(f"\n{reason}")
    print("You have failed to escape the Cursed Library.")
    print(f"\nYour journey: {' → '.join(player_choices)}")
    quit()

def win_game():
    """Handle winning scenario and end the game"""
    print("\nYou burst through the library doors just as the first rays of sunlight pierce the horizon!")
    print("The library fades behind you like a forgotten dream.")
    print("You are free!")
    print(f"\nYour journey: {' → '.join(player_choices)}")
    quit()

# --- Main Game Function ---

def main():
    """Main game logic containing the story and decision tree"""
    global candles_remaining, player_choices, has_key
    
    # --- Story Introduction ---
    print("=" * 60)
    print("THE CURSED LIBRARY")
    print("=" * 60)
    print("\nYou are a university student researching late at night.")
    pause()
    print("At the stroke of midnight, you discover a door in the library")
    print("that wasn't there before...")
    pause()
    print("Curiosity pulls you through, and the door slams shut behind you.")
    pause()
    print("\nYou're now in an ancient library lit only by flickering candles.")
    print("A grandfather clock chimes: 'Escape before sunrise, or remain forever.'")
    pause()
    show_candles()
    
    # --- Layer 1: Initial Decision ---
    print("\nYou see three aisles stretching before you:")
    print("1. The History Section - dusty tomes line wooden shelves")
    print("2. The Fiction Section - colorful books seem to glow faintly")
    print("3. The Forbidden Section - chained books emanate dark energy")
    
    choice1 = input("> ").strip()
    player_choices.append(f"Aisle-{choice1}")
    extinguish_candle()
    time_passes()
    show_candles()
    
    # --- Branch A: History Section ---
    if choice1 == "1":
        print("\nYou walk down the History aisle.")
        pause()
        print("An old journal falls from a shelf. Its pages show a map of the library")
        print("and a riddle: 'The way out lies where stories began.'")
        pause()
        mysterious_whisper()
        pause()
        
        # --- Layer 2A: History Exploration ---
        print("\nDo you:")
        print("1. Search for the oldest book in the section.")
        print("2. Follow the map to the library's center.")
        
        choice2 = input("> ").strip()
        player_choices.append(f"History-{choice2}")
        extinguish_candle()
        time_passes()
        show_candles()
        
        # Path A1: Search for oldest book
        if choice2 == "1":
            print("\nYou find a crumbling book titled 'Genesis of Knowledge.'")
            pause()
            print("Inside, a silver key falls out!")
            has_key = True
            print("You've obtained the Silver Key!")
            pause()
            
            # --- Layer 3A: Key Decision ---
            print("\nA locked door appears before you. Do you:")
            print("1. Use the silver key immediately.")
            print("2. Continue exploring to ensure it's the right door.")
            
            choice3 = input("> ").strip()
            player_choices.append(f"Key-{choice3}")
            
            if choice3 == "1":
                print("\nThe key turns smoothly. The door opens to reveal...")
                pause()
                print("A janitor's closet. Wrong door!")
                game_over("You wasted your only key. You're trapped forever.")
            elif choice3 == "2":
                print("\nYou explore further and find the TRUE exit door.")
                pause()
                print("The silver key fits perfectly!")
                win_game()
            else:
                game_over("You hesitate too long. The key crumbles to dust in your hands.")
        
        # Path A2: Follow map to center
        elif choice2 == "2":
            print("\nYou reach the library's center: a circular room with a massive book on a pedestal.")
            pause()
            print("The book is titled 'Liber Exitium' - The Book of Escape.")
            pause()
            print("It asks: 'What do all stories need to exist?'")
            
            # --- Layer 3A2: Riddle Decision ---
            print("\nDo you answer:")
            print("1. A reader")
            print("2. An ending")
            
            choice3 = input("> ").strip()
            player_choices.append(f"Riddle-{choice3}")
            
            if choice3 == "1":
                print("\nThe book glows with golden light!")
                pause()
                print("'Correct. Stories exist only when someone reads them.'")
                pause()
                print("A portal opens before you!")
                win_game()
            elif choice3 == "2":
                game_over("The book slams shut. 'Wrong! Not all stories end.' You're sealed inside.")
            else:
                game_over("The book grows impatient and traps you within its pages.")
        
        else:
            game_over("You knock over a candelabra. The fire spreads quickly. Game over.")
    
    # --- Branch B: Fiction Section ---
    elif choice1 == "2":
        print("\nYou enter the Fiction section.")
        pause()
        print("The books are whispering stories. One book falls open before you:")
        print("'The Tale of the Trapped Scholar.'")
        pause()
        print("It's about someone just like you, stuck in this very library!")
        pause()
        
        # --- Layer 2B: Fiction Exploration ---
        print("\nDo you:")
        print("1. Read the book to find out how they escaped.")
        print("2. Close the book and look for a more direct exit.")
        
        choice2 = input("> ").strip()
        player_choices.append(f"Fiction-{choice2}")
        extinguish_candle()
        time_passes()
        show_candles()
        
        # Path B1: Read the book
        if choice2 == "1":
            print("\nYou read frantically. The story says:")
            print("'The scholar realized the library was a story itself.'")
            pause()
            print("'To escape, one must become the author, not the character.'")
            pause()
            
            # --- Layer 3B1: Reality Decision ---
            print("\nA glowing pen appears. Do you:")
            print("1. Write 'THE END' in the air.")
            print("2. Write 'I am the author of my story' in the air.")
            
            choice3 = input("> ").strip()
            player_choices.append(f"Writing-{choice3}")
            
            if choice3 == "1":
                game_over("Everything goes black. You ended the story... with you still in it.")
            elif choice3 == "2":
                print("\nThe words shimmer and glow!")
                pause()
                print("Reality bends around you. You're rewriting the story!")
                pause()
                print("You write: 'And the student walked through the exit door.'")
                pause()
                print("A door materializes!")
                win_game()
            else:
                game_over("The pen fades away. Your indecision has sealed your fate.")
        
        # Path B2: Look for direct exit
        elif choice2 == "2":
            print("\nYou spot a glowing EXIT sign through the shelves.")
            pause()
            print("But wait... it's moving, floating between the books like a firefly.")
            pause()
            
            # --- Layer 3B2: Chase Decision ---
            print("\nDo you:")
            print("1. Chase the EXIT sign quickly.")
            print("2. Follow it slowly and carefully.")
            
            choice3 = input("> ").strip()
            player_choices.append(f"Exit-{choice3}")
            
            if choice3 == "1":
                game_over("You run after it and fall through a hidden trapdoor into eternal darkness.")
            elif choice3 == "2":
                print("\nYou follow patiently. The sign leads you through a maze of shelves.")
                pause()
                print("Finally, it stops at a small door you hadn't noticed before.")
                pause()
                print("The door is unlocked!")
                win_game()
            else:
                game_over("You lose sight of the exit sign and wander lost until sunrise.")
        
        else:
            game_over("A character from a book steps out and pulls you into their story forever.")
    
    # --- Branch C: Forbidden Section ---
    elif choice1 == "3":
        print("\nYou approach the Forbidden Section.")
        pause()
        print("The chains rattle and fall away as you get closer.")
        print("A voice echoes: 'Few dare enter here. Fewer leave.'")
        pause()
        mysterious_whisper()
        pause()
        
        # --- Layer 2C: Forbidden Exploration ---
        print("\nTwo books are glowing:")
        print("1. 'The Book of Shadows' - bound in black leather")
        print("2. 'The Book of Light' - bound in white silk")
        
        choice2 = input("> ").strip()
        player_choices.append(f"Forbidden-{choice2}")
        extinguish_candle()
        time_passes()
        show_candles()
        
        # Path C1: Book of Shadows
        if choice2 == "1":
            print("\nYou open the Book of Shadows.")
            pause()
            print("It shows you your deepest fear: being trapped forever.")
            print("But then it whispers: 'Face your fear, and it has no power.'")
            pause()
            
            # --- Layer 3C1: Fear Decision ---
            print("\nDo you:")
            print("1. Close your eyes and accept the fear.")
            print("2. Throw the book away and run.")
            
            choice3 = input("> ").strip()
            player_choices.append(f"Shadows-{choice3}")
            
            if choice3 == "1":
                print("\nYou stand firm, eyes closed, facing your fear.")
                pause()
                print("When you open your eyes, the library is gone.")
                pause()
                print("You're standing outside in the cool night air.")
                win_game()
            elif choice3 == "2":
                game_over("Your fear chases you. You can never outrun yourself.")
            else:
                game_over("The book consumes your hesitation and you become a shadow yourself.")
        
        # Path C2: Book of Light
        elif choice2 == "2":
            print("\nYou open the Book of Light.")
            pause()
            print("Blinding radiance fills the room. The voice speaks:")
            print("'Answer truly: Why did you enter this library?'")
            pause()
            
            # --- Layer 3C2: Truth Decision ---
            print("\nDo you answer:")
            print("1. I was curious and made a mistake.")
            print("2. I seek knowledge, whatever the cost.")
            
            choice3 = input("> ").strip()
            player_choices.append(f"Light-{choice3}")
            
            if choice3 == "1":
                print("\nThe light softens. The voice says: 'Honesty is the first step to freedom.'")
                pause()
                print("The library releases you from its grip.")
                win_game()
            elif choice3 == "2":
                game_over("'Then stay and learn forever.' You become the library's eternal student.")
            else:
                game_over("The light burns too bright. You vanish in the radiance.")
        
        else:
            game_over("You touch both books at once. They cancel each other out, and you with them.")
    
    else:
        game_over("You panic and stumble in the darkness. You never find your way out.")

# --- Program Entry Point ---
if __name__ == "__main__":
    # Welcome message
    print("Welcome to THE CURSED LIBRARY")
    print("A mysterious adventure awaits...")
    print()
    
    
    while True:
        candles_remaining = MAX_CANDLES
        player_choices = []
        has_key = False
        main()
        
        # Ask to play again
        play_again = input("\nWould you like to explore the library again? (yes/no): ").strip().lower()
        
        
        if play_again == "yes" or play_again == "y":
            print("\nThe library door appears once more...\n")
            continue
        elif play_again == "no" or play_again == "n":
            print("\nThank you for playing THE CURSED LIBRARY!")
            print("Sleep well... if you can.")
            break
        else:
            print("\nInvalid input. The library fades away...")
            break
