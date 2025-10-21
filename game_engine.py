from dataclasses import dataclass, field
from typing import List, Tuple
from eval import safe_eval
import random
from enum import Enum, auto

# Differentiate between the two phases of the game
class Phase(Enum):
    PICK   = auto()   # user is still choosing the 6 numbers
    SOLVE  = auto()   # user is trying to hit the target

# User input handling
def prompt(message: str) -> str:
    """
    Print message (if any) and read a line from stdin.
    Strip whitespace and lowercase the result for uniform handling.
    """
    return input(message).strip().lower()

# Set of acceptable large number values
larges = [25,50,75,100]
# Set of acceptable small number values
smalls = [1,2,3,4,5,6,7,8,9,10]

# Function to randomly pick a large number and add it to the target set
def pick_large(picks: List[int]):
    randindex = random.randint(0,len(larges)-1)
    picks.append(larges[randindex])
    print(larges[randindex])

# Function to randomly pick a small number and add it to the target set
def pick_small(picks: List[int]):
    randindex = random.randint(0,len(smalls)-1)
    picks.append(smalls[randindex])
    print(smalls[randindex])

# Game class and methods
@dataclass
class Game:
    target: int = 0
    picks: List[int] = field(default_factory=list)
    round_number: int = 1
    phase: Phase = Phase.PICK
    wins: int = 0

    # Automatically set the random target when a fresh Game is initiated
    @staticmethod
    def new_game() -> "Game":
        """Factory that creates a fresh game with a random target."""
        return Game(target=random.randint(1, 999))

    # Reset but keep the same Game object 
    def reset(self) -> None:
        """Reset everything but keep the same object (useful for `r`)."""
        self.target = random.randint(1, 999)
        self.picks.clear()
        self.round_number = 1
        self.phase = Phase.PICK

    # Allow user to add operands to the picks set (PICK phase)
    def add_random_large(self) -> None:
        self.picks.append(random.choice(larges))
        print(f"Added large number → {self.picks[-1]}")

    def add_random_small(self) -> None:
        self.picks.append(random.choice(smalls))
        print(f"Added small number → {self.picks[-1]}")

    # Evaluate submitted expressions (SOLVE phase)
    def submit_expression(self, expr: str) -> Tuple[bool, str]:
        """Return (success, message)."""
        try:
            value = safe_eval(expr, self.picks)
        except ValueError as err:
            return False, f"Invalid expression: {err}"
        
        # Incorrect guess bumps up round number
        if value != self.target:
            self.round_number += 1
            return False, f"Result {value} does not match target {self.target}. Try again! \n Guesses remaining: {10 - self.round_number}"
            
        # If we get here the expression is correct
        self.wins += 1
        return True, f"Well done! 🎉\n Enter r to play again or q to quit."
    
    # TODO: rejig this to work with the refactored game logic
    def game_over(self) -> None:
        # Stop after 10 rounds if the player still hasn't solved it
        if self.round_number > 10:
            print(f"Out of guesses! Better luck next time")
        self.reset()
