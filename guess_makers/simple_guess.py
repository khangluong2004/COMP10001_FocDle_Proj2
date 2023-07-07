# Task 4 - Simple, random guess
# Used along with restrictions validator to keep 
# generating guesses until pass the restrictions
# or some limit has been reached (> n guesses).

# Example:
# GCOUNT_MAX = 10000
# while True:
#     new_guess = create_guess(all_info, difficulty)
#     if passes_restrictions(new_guess, all_info):
#         # seems like it might be a good guess
#         break
#     gcount += 1
#     if gcount > GCOUNT_MAX:
#         # just use this guess anyway
#         break

import random

GREEN = "green"
YELLOW = "yellow"
GREY = "grey"
DEF_DIFFIC = 10
OPERATORS = "+-*%"
EQUALITY = "="
DIGITS = "0123456789"
POSSIBLE_CHAR = OPERATORS + EQUALITY + DIGITS

def create_guess(all_info: list, difficulty: int=DEF_DIFFIC) -> str:
    '''
    Takes information built up from past guesses that is stored in `all_info`, 
    and uses it as guidance to generate a new guess of length `difficulty`.
    Return the generated guess (str)
    '''
    # possible_vals: A list storing a set of possible characters
    #   at the corresponding position in the guess 
    #   (eg: possible chars for position 2 in guess is stored
    #   at index 2 in the list)
    possible_vals = [set(POSSIBLE_CHAR) for i in range(difficulty)]
    
    # Check all the info entry in all_info: 
    # 1. If there is a green char at position ith, only 
    #   that char is possible at position ith
    # 2. If there is a yellow or grey char at position ith, 
    #   that char is not possible at position ith 
    for sublist_info in all_info:
        for position_info in sublist_info:
            position, char, color = position_info
            if color == GREEN:
                possible_vals[position] = {char}
            else:
                possible_vals[position].discard(char)

    # Generate the guess by pick randomly a possible char
    # at each position
    guess = "".join([random.choice(tuple(possible_val)) 
                     for possible_val in possible_vals])
    return(guess)