# Countdown Numbers Game

Author: jarilaitinen
Version: 1.0.2

This little Python program lets you play the arithmetic game from Countdown. I'm learning Python after being primarily a JS/TS and Wordpress developer - if you are experienced with Python or game development please feel free to suggest improvements! 

## Game rules

You have six operands - you can pick a large integer (25, 50, 75 or 100, chosen randomly by the game) or a small integer (1-10) in each case. The game picks a target between 1 and 999 and your task is to use simple arithmetic (+, -, *, /) to make a statement using the operands which is equal to the target. Each operand may be used only once (if the same integer appears twice in the operand set, it may be used twice). Parentheses are allowed. 

Example: 

You pick two large operands and four small operands. The game gives you an operand list of [50, 50, 8, 2, 9, 7] and a target of 955. 

A valid puzzle solution could be: 

> (50 + 50 + 7) * 9 - 8

## Currently implemented features

As of v 1.0.2:
- Allows users to pick large or small operands and generates a new puzzle.
- Verifies that user input contains only integers from the puzzle set, allowed operators and parentheses, and that the number of operands in the user entry is not greater than the number in the puzzle set. Displays an error message if the input is invalid.
- After verifying the validity of the user input, evaluates the expression and checks if it matches the target. Displays a win message if the solution is correct and an error message if the expression does not evaluate to the target.
- Game ends automatically after 10 failed attempts!
- Now tracks how many puzzles you've successfully solved in the allowed attempts. When you quit, it shows you your score!
- Quit (q), reset (r) or get instructions (h) at any time.


## To-do

- Find all possible solutions to the generated puzzle; eliminate impossible puzzles. Show alternate solutions after quit or solve.
- Give an option for hint after a failed attempt (in the format of two operands + operator from a valid solution)
- Make a slightly fancier UI 
- Perhaps allow for a user name and timer to track solve time and number of attempts... allow exporting these details to CSV
- Optional Clock Mode with animated clock and time limit for the masochistic

## Changelog

__26.10.2025: v1.0.2__ Refactored game loop, eliminated duplicated input() calls and nested whiles from game loop, improved switching between game states (pick vs solve) and removed the global list variable from eval.py. Added an expanded instruction guide behind the h command.