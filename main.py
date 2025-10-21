import sys
from typing import Any, Callable, Dict, List, Set
from game_engine import Game, prompt, Phase

# Handle special commands
def handle_control(command: str, game: Game) -> bool:
    """
    Return True if the loop should continue after handling the command,
    False if the loop should break (i.e. quit).

    TODO: hint feature
    """
    cmd = command.lower()
    if cmd in {"quit", "exit", "q"}:
        print(f"You successfully solved {game.wins} puzzles. See you later!")
        sys.exit(0)               # clean termination
    if cmd == "r":
        # Reset the game object
        game.reset()
        print("\n--- Game reset ---")
        return True
    if cmd == "h":
        print("""\n--- HELP -------------------------------------------------
        Pick numbers:
            L – add a random *large* number (25, 50, 75, 100)
            S – add a random *small* number (1‑10)

        When you have 6 numbers, a *target* (1‑999) is shown.
        Enter a mathematical expression that uses **only** those numbers
        (and the operators +, -, *, //).  Parentheses are allowed.

        Special commands:
            r – reset the game
            q – quit
        -------------------------------------------------------------------""")
        return True
    # DEBUG COMMANDS
    # Show current puzzle variables
    if cmd == "stats":
        print(f"Puzzle set {game.picks}")
        print(f"Game phase {game.phase}")
        print(f"Solved puzzles {game.wins}")
        return True
    else:
        return False

def game_loop() -> None:
    game = Game.new_game()

    # Greet the user
    print("Welcome to the Countdown number puzzle!")
    print("q to quit - r to reset - h for help")

    while True: 
        if game.phase is Phase.PICK:
            if len(game.picks) == 6:
                game.phase = Phase.SOLVE
                print("\n--- Numbers ready ---")
                print(f"Puzzle set: {game.picks}")
                print(f"Target: {game.target}\n")
                continue  #  
            raw = prompt("Pick a number (L/S) > ")
        else:  # Phase.SOLVE
            raw = prompt("Enter expression > ")

        # Global commands (quit / reset / help)
        if handle_control(raw, game):
            continue

        # Phase-specific handling
        if game.phase is Phase.PICK:
            if raw == "l":
                game.add_random_large()
            elif raw == "s":
                game.add_random_small()
            else:
                print("Invalid choice – type L or S.")
            
        else: # Phase.SOLVE
            success, msg = game.submit_expression(raw)
            print(msg)
        

def main() -> None:
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nInterrupted – exiting.")
        sys.exit(0)

main()



