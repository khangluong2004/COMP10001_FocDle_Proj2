#DEPRECATED - Poor performances

import random
from itertools import product
from project2_helper_functions import *
# Task 5 - Better guess
GREEN = "green"
YELLOW = "yellow"
GREY = "grey"
DEF_DIFFIC = 10
OPERATORS = "+-*%"
EQUALITY = "="
DIGITS = "0123456789"
POSSIBLE_CHAR = OPERATORS + EQUALITY + DIGITS

# Position-wise approach
def create_better_guess_position(all_info, difficulty=DEF_DIFFIC):
    '''
    Takes information built up from past guesses that is stored in `all_info`,
    and uses it as guidance to generate a new guess of length `difficulty`.
    '''
    # Parsing all_info:

    # Making a list of possible value
    possible_vals = [set(DIGITS) for _ in range(difficulty)]
    op1_positions = {x for x in (1, 2) if x <= difficulty - 6}
    op2_positions = {x for x in (3, 4, 5) if x <= difficulty - 4}
    equal_positions = {x for x in (5, 6, 7, 8) if x <= difficulty - 2}
    for op_position in (op1_positions | op2_positions):
        possible_vals[op_position] |= (set(OPERATORS))
    for equal_position in equal_positions:
        possible_vals[equal_position] |= {EQUALITY}
    for sublist_info in all_info:
        for position_info in sublist_info:
            position, char, color = position_info
            if color == GREEN:
                possible_vals[position] = {char}
            else:
                possible_vals[position].discard(char)

    guess = ["" for i in range(difficulty)]
    num_op = 0
    check_op = False
    # Check green
    all_green = set()
    for i in range(difficulty):
        if len(possible_vals[i]) == 1:
            all_green.add(i)
            guess[i] = possible_vals[i].pop()
            if not check_op and guess[i] in OPERATORS:
                num_op += 1
                if num_op >= 2:
                    check_op = True

    for i in range(difficulty):
        if i not in all_green:
            if EQUALITY in guess:
                possible_vals[i] -= {EQUALITY}
            if check_op:
                possible_vals[i] -= set(OPERATORS)
            guess[i] = random.choice(tuple(possible_vals[i]))
            if not check_op and (guess[i] in OPERATORS):
                num_op += 1
                if num_op >= 2:
                    check_op = True
    guess = "".join(guess)
    return(guess)