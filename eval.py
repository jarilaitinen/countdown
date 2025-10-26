"""
    Evaluation helper to safely determine the validity of user input and 
    1. Tokenise & parse the raw string with ast.parse(..., mode='eval').
    2. Validate the resulting AST:
        Every Constant must be an integer and be present in picks set.
        Every node must be one of the whitelisted types (BinOp, Expression, Paren).
        The operator used must be in the safe operator map.
    3. Evaluate the validated tree by recursively applying the corresponding functions from the operator module.
    4. Compare the computed value with the target; report success/failure.
"""
import ast
import operator
from typing import Any, Callable, Dict, List, Set

# Only allow addition, subtraction, multiplication and division with no remainder
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.FloorDiv: operator.floordiv,
}

# Map AST operator classes → the actual Python function that performs it
_OP_MAP: Dict[type, Callable[[int, int], int]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.FloorDiv: operator.floordiv,
}

# Validator class - check node for disallowed characters
class _Validator(ast.NodeVisitor):
# Allow safe_init to pass the set of allowed integers
    def __init__(self, allowed_numbers: set[int]) -> None:
        self.allowed_numbers = allowed_numbers
# Validate constants
    def visit_Constant(self, node: ast.Constant) -> None:
# Don't allow non-integers!
        if not isinstance(node.value, int):
            raise ValueError("Only integers in the puzzle set are allowed.")
# Don't allow integers not in allowed_ints!
        if node.value not in self.allowed_numbers:
            raise ValueError(f"The number {node.value} is not part of the puzzle set.")
# Validate binops
    def visit_BinOp(self, node: ast.BinOp) -> None:
# Don't allow operators not in _ALLOWED_OPS!
        if type(node.op) not in _ALLOWED_OPS:
            raise ValueError(f"Operator {type(node.op).__name__} not allowed.")
        self.generic_visit(node)
# The top‑level Expression node (produced by ast.parse(mode='eval'))
    def visit_Expression(self, node: ast.Expression) -> None:
        self.generic_visit(node)
# Disallow anything else!
    def generic_visit(self, node: ast.AST) -> None:
        if isinstance(node, ast.operator):
            return  # nothing to validate – they are already checked in visit_BinOp
        if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant)):
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        super().generic_visit(node)

# Evaluate each node of the user input
def _evaluate(node: ast.AST) -> int:
    if isinstance(node, ast.Constant):
        return node.value # type: ignore

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        func = _OP_MAP[type(node.op)]
        return func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        func = _OP_MAP[type(node.op)]
        return func(operand) # type: ignore

    # Should never reach here because the validator blocks everything else
    raise RuntimeError(f"Unexpected node type during evaluation: {type(node).__name__}")

# Evaluate the user's input
def safe_eval(expr: str, picks: List[int]) -> int:
    """
    Evaluate *expr* safely.
    • Only integer literals from ALLOWED_NUMBERS may appear.
    • Only the operators listed in _OP_MAP are permitted.
    • Parentheses are allowed; any other syntax raises ValueError.
    Returns the integer result.
    """

    # Make an immutable set with the user picks
    allowed_set = set(picks)
    # Parse the expression (throws SyntaxError if it isn’t valid Python)
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc.msg}")
    # Validate the tree
    _Validator(allowed_set).visit(tree)
    # Count how many numeric literals were used (enforce 2‑to‑6 rule)
    # Counter class increments self.count every time it encounters a node of type int
    class _Counter(ast.NodeVisitor):
        def __init__(self):
            self.count = 0
        def visit_Constant(self, node):
            if isinstance(node.value, int):
                self.count += 1

    counter = _Counter()
    counter.visit(tree) 
    # If the number of operands is less than two or more than six, raise an error
    if not (2 <= counter.count <= 6):
        raise ValueError(
            f"You must use between 2 and 6 numbers; found {counter.count}."
        )
    
    # Evaluate safely
    try:
        result = _evaluate(tree.body)   # tree.body is the inner expression node
    except ZeroDivisionError:
        raise ValueError("Division by zero is not allowed.")

    return result


"""
CHECKS
---
print(safe_eval("2*8-2"))  # → 14
print(safe_eval("5+9"))     # → 14
print(safe_eval("2*3+3+5")) # → 14
print(safe_eval("2*(3+8)+5")) # 27
print(safe_eval("2-3+(5*8)-9+6")) # 36
print(safe_eval("2*3+7+5")) # fail - not in puzzle set
print(safe_eval("2-3+(5*8)-9+6+3")) # fail - too many operands
print(safe_eval("dfklj_")) # fail - invalid syntax
"""

