import random
import sys
from typing import Any, Callable, Dict, List, Set
from game_engine import Game

# Initialise the game state
def initialise_game() -> Game:
    target = random.randint(1, 999)     # Random target between 1 and 999
    picks = []                          # List for user-chosen operands
    round = 1
    return Game(target=target, picks=picks, round_number=round)


# Handle special commands to quit or reset the game
def handle_control(command: str, game: Game) -> bool:
    """
    Return True if the loop should continue after handling the command,
    False if the loop should break (i.e. quit).

    TODO: hint feature
    """
    cmd = command.lower()
    if cmd in {"quit", "exit", "q"}:
        print("See you later!")
        sys.exit(0)               # clean termination
    elif cmd == "r":
        # Reset the game object
        new_game = initialise_game()
        game.__dict__.update(new_game.__dict__)   # shallow copy of attributes
        print("Game has been reset.")
        return True
    elif cmd == "h":
        print("---\nUse L or S to choose random large or small numbers for the puzzle set.\nThen enter a mathematical expression using simple arithmetic and the numbers in the set to reach the target.\nParentheses are allowed - the game evaluates expressions using standard order of operations.\nEnter r to reset the game or q to quit.\n---")
        return True
    else:
        return False

def game_loop(game: Game) -> None:
    while not game.is_finished(): 
        while len(game.picks) < 6:
            print("Pick L or S")
            user_input = input("> ").strip() # TODO: Can I avoid this redundancy somehow?
            # Check for special commands first
            if handle_control(user_input, game):        
                continue
            # Pick operands for the puzzle set
            game.pick_operands(user_input, game.picks)
        
        print(f"Puzzle operands: {game.picks}")
        print(f"Target is {game.target}. Enter an expression:")   
        user_input = input("> ").strip()
        # Check for special commands first
        if handle_control(user_input, game):        
            continue
        success, msg = game.submit_expression(user_input, game.picks)
        # If the user's input is correct, run the success condition and ask them to input a command to play again or quit.
        if success == True:
            print(msg)
            user_input = input("> ").strip()
            if handle_control(user_input, game):        
                continue
        # If the user's input is incorrect, run the failure condition and ask them to guess again. 
        else:
            print(msg)
        

def main() -> None:
    try:
        # Initialise the game state
        game = initialise_game()
        # Greet the user
        print("Welcome to the Countdown number puzzle!")
        print("q to quit - r to reset - h for help")
        # Launch the loop
        game_loop(game)
    except KeyboardInterrupt:
        print("\nInterrupted – exiting.")
        sys.exit(0)

main()



