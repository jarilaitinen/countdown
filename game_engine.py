from dataclasses import dataclass, field
from typing import List, Tuple
from eval import safe_eval
import random

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

# Game class
@dataclass
class Game:
    target: int
    picks: List[int]
    round_number: int

    def pick_operands(self, expr: str, picks):
        if expr == "L":
            pick_large(picks)
        elif expr == "S":
            pick_small(picks)
        else:
            print('Not a valid input')

    def submit_expression(self, expr: str, picks) -> Tuple[bool, str]:
        """Return (success, message)."""
        try:
            value = safe_eval(expr, picks)
        except ValueError as err:
            return False, f"Invalid expression: {err}"
        if value != self.target:
            self.round_number += 1
            return False, f"Result {value} does not match target {self.target}. Try again!"
            
        # If we get here the expression is correct
        self.round_number += 1
        return True, f"Well done! 🎉\n Enter r to play again or q to quit."
    
    def is_finished(self) -> bool:
        # Placeholder: stop after 10 rounds for demo purposes
        return self.round_number > 10
