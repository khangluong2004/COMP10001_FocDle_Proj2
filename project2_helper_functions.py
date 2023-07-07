# Task 1 - Secret gen
import random

DEF_DIFFIC = 10
MAX_TRIALS = 60
MAX_VALUE = 99
MIN_VALUE = 1
OPERATORS = "+-*%"
EQUALITY = "="
DIGITS = "0123456789"
NOT_POSSIBLE = "No FoCdle found of that difficulty"

def create_secret(difficulty=DEF_DIFFIC):
    '''
    Use a random number function to create a FoCdle instance of length 
    `difficulty`. The generated equation will be built around three values 
    each from 1 to 99, two operators, and an equality.
    '''
    for _ in range(MAX_TRIALS):
        # Choose 2 operator and 3 values randomly in the appropriate
        # range and avaialable characters
        operators = [str(random.choice(OPERATORS)) for _ in range(2)]
        values = [str(random.randint(MIN_VALUE, MAX_VALUE)) for _ in range(3)]
        # Arrange the operators to create the first part before = in the secret
        equation = values[0] + operators[0] + values[1] + operators[1] +\
            values[2]
        result = eval(equation)

        # Ensure the result is positive and has the desirable length before 
        # returning the secret
        if result <= 0:
            continue
        secret = f"{equation}{EQUALITY}{result}"
        if len(secret) == difficulty:
            return(secret)
        
    return(NOT_POSSIBLE)

# Task 2 - Set colour
GREEN = "green"
YELLOW = "yellow"
GREY = "grey"

def parse_info_ordered(phrase: str) -> dict:
    ''' 
    Receive the `phrase` as argument, and return a chars_info dictionary 
    with key = character and value= positions of that char: list
    '''
    chars_info = {}
    for i in range(len(phrase)):
        if phrase[i] in chars_info:
            chars_info[phrase[i]].append(i)
        else:
            chars_info[phrase[i]] = [i]
    return(chars_info)

def set_colors(secret: str, guess: str) -> list:
    '''
    Compares the latest `guess` equation against the unknown `secret` one. 
    Returns a list of three-item tuples, one tuple for each character position 
    in the two equations:
        -- a position number within the `guess`, counting from zero;
        -- the character at that position of `guess`;
        -- one of "green", "yellow", or "grey", to indicate the status of
           the `guess` at that position, relative to `secret`.
    The return list is sorted by position.
    '''
    # Parse and store positions of each char in a dict
    # with key = character and value = positions of the char: list
    # secret_info: Dict for secret info
    # guess_info: Dict for guess info
    secret_info = parse_info_ordered(secret)
    guess_info = parse_info_ordered(guess)
    # color_list: The 2D-list, initiliazed with 
    # [position, character at that position, color = grey]
    color_list = [[i, guess[i], 'grey'] for i in range(len(guess))]
    for char in guess_info:
        if char in secret_info:
            # For each char, find the positions in the guess that
            # appears in the secret, then set it to green.
            # all_green: A set of correct positions in guess
            all_green = set(secret_info[char]) & set(guess_info[char])
            for green_position in all_green:
                color_list[green_position][2] = GREEN
            
            # Check if the character in guess also appears else where
            if len(guess_info[char]) > len(all_green):
                # Find the number of yellow 
                # = All_positions (in secret) - Green positions (in guess) 
                number_yellow = len(secret_info[char]) - len(all_green)
                # Mark yellow the `number_yellow` characters that is not 
                # in correct positions from left to right
                for position in guess_info[char]:
                    if number_yellow == 0:
                        break
                    elif position not in all_green:
                        color_list[position][2] = YELLOW
                        number_yellow -= 1

    # Convert `color_list` to the list of tuple as required
    return(list(map(tuple, color_list)))