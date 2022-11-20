# Implanted from: https://realpython.com/python-eval-function/

"""
    This file is an expression parser which is used to parse the election
    voting formula inputted in the backend.
    For a particular election, the formula is used to calculate the 
    voting ratio of each candidate.
    The formula is a mathematical expression which should be only consist of
    the methods or operators defined under the math module.
    Moreover, the variables indicating "kisa_in_debate_votes_[all/my]", "kisa_out_of_debate_votes_[all/my]",
    "non_kisa_votes_[all/my]" are allowed to be used too. The corresponding variable
    names are "kiva", "kivm", "kova", "kovm", "nkva" and "nkvm" respectively.
"""

import math

ALLOWED_NAMES = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}

def get_evaluation(expression, **kwargs):
    """Evaluate a math expression."""
    # Compile the expression
    code = compile(expression, "<string>", "eval")
    
    allowed_names_all = ALLOWED_NAMES | kwargs

    # Validate allowed names
    for name in code.co_names:
        if name not in allowed_names_all:
            raise NameError(f"The use of '{name}' is not allowed")

    return eval(code, {"__builtins__": {}}, allowed_names_all)

def evaluate(expression, **kwargs):
    try:
        result = get_evaluation(expression, **kwargs)
        return (True, result)
    except SyntaxError:
        # If the user enters an invalid expression
        return (False, "Invalid input expression syntax")
    except (NameError, ValueError) as err:
        # If the user tries to use a name that isn't allowed
        # or an invalid value for a given math function
        return (False, err)

