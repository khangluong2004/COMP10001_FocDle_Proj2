from itertools import product
import random
import copy

from pre_calc_info.freq_result import FREQ_TABLE

GREEN = "green"
YELLOW = "yellow"
GREY = "grey"
DEF_DIFFIC = 10
OPERATORS = "+-*%"
EQUALITY = "="
DIGITS = "0123456789"
POSSIBLE_CHAR = OPERATORS + EQUALITY + DIGITS
FIRST_GUESS = {7: '+-*%1=1', 8: '1-*%+==1', 9: '1*-+%===1', 10: '27-1+%===*', 11: '5*-2+%===10', 12: '9+31*2-==10%', 13: '9%+9*-9==1000', 14: '1+-1%*10=32000', 15: '9+-99*99=10%200'}


def parse_info_unordered(phrase: str) -> dict:
    ''' 
    Receive the `phrase` as argument, and return a chars_info dictionary 
    with key = character and value=positions: set 
    '''
    chars_info = {}
    # Fill the chars_info for each char in secret
    for i in range(len(phrase)):
        if phrase[i] in chars_info:
            chars_info[phrase[i]].add(i)
        else:
            chars_info[phrase[i]] = {i}
    return(chars_info)

def parse_all_info(all_info: list, difficulty: int) -> tuple:
    ''' Parse all info, and return (check_info, all_green)'''
    # Parsing all_info
    # check_info: Dictionary with key=char, 
    # value={exact_positions: set, possible_positions: set, 
    # min_count: int, max_count: int}
    # guess_info: Dictionary with key=char, value=positions: set
    # check_info: Dictionary with key=char, 
    # value={exact_positions: set, possible_positions: set, 
    # min_count: int, max_count: int}
    valid_char = set(POSSIBLE_CHAR)
    valid_opp = set()
    all_values = set(range(difficulty)) 
    op1_positions = {x for x in (1, 2) if x <= difficulty - 6}
    op2_positions = {x for x in (3, 4, 5) if x <= difficulty - 4}
    op_positions = op1_positions | op2_positions
    equal_positions = {x for x in (5, 6, 7, 8) if x <= difficulty - 2}
    max_possible = difficulty - 3
    check_info = {}
    all_green = set()
    for sublist in all_info:
        # sublist_info: Dictionary with key=char, value={exact_positions: set, 
        # possible_positions: set, min_count: int, max_count: int}
        sublist_info = {}
        for char_info in sublist:
            curr_position, curr_char, curr_color = char_info
            if curr_char not in sublist_info:
                max_value = max_possible
                possible_postions = all_values
                if curr_char in OPERATORS:
                    max_value = 2
                    possible_postions = op_positions
                    if curr_color in (GREEN, YELLOW):
                        valid_opp.add(curr_char)
                elif curr_char == EQUALITY:
                    max_value = 1
                    possible_postions = equal_positions
                if curr_color == GREEN:
                    sublist_info[curr_char] = \
                        {"exact_positions": {curr_position}, 
                         "possible_positions": possible_postions - {curr_position}, 
                         "min_count": 1, "max_count": max_value}
                    all_green.add(curr_position)
                elif curr_color == YELLOW:
                    sublist_info[curr_char] = \
                        {"exact_positions": set(), 
                         "possible_positions": possible_postions - {curr_position}, 
                         "min_count": 1, "max_count": max_value}
                else:
                    sublist_info[curr_char] = {"exact_positions": set(), 
                                               "possible_positions": set(), 
                                               "min_count": 0, "max_count": 0}
                    valid_char.discard(curr_char)
            else:
                if curr_color == GREEN:
                    sublist_info[curr_char]["exact_positions"].add(
                        curr_position)
                    sublist_info[curr_char]["possible_positions"].discard(
                        curr_position)
                    prev_min = sublist_info[curr_char]["min_count"]
                    sublist_info[curr_char]["min_count"] += 1
                    # If encountered a grey before (recognize by max = min), 
                    # we need to adjust the count accordingly
                    if sublist_info[curr_char]["max_count"] == prev_min:
                        sublist_info[curr_char]["max_count"] = \
                            sublist_info[curr_char]["min_count"]
                        # Restore validity if grey before
                        valid_char.add(curr_char)
                    all_green.add(curr_position)
                elif curr_color == YELLOW:
                    sublist_info[curr_char]["possible_positions"].discard(
                        curr_position)
                    sublist_info[curr_char]["min_count"] += 1
                else:
                    sublist_info[curr_char]["possible_positions"].discard(
                        curr_position)
                    sublist_info[curr_char]["max_count"] = \
                        sublist_info[curr_char]["min_count"]
        for char in sublist_info:
            if char not in check_info:
                check_info[char] = sublist_info[char]
            else:
                check_info[char]["exact_positions"] |= \
                    sublist_info[char]["exact_positions"]
                check_info[char]["possible_positions"] &= \
                    sublist_info[char]["possible_positions"]
                check_info[char]["min_count"] = \
                    max(check_info[char]["min_count"], 
                        sublist_info[char]["min_count"])
                check_info[char]["max_count"] = \
                    min(check_info[char]["max_count"], 
                        sublist_info[char]["max_count"])
    
    # Compute guarantee_taken places from the minimum apperance of each digit
    # and the guarantee_operator for minimum appearance of each operators
    guarantee_taken = 0
    guarantee_operator = 0
    for char in check_info:
        if char in OPERATORS:
            guarantee_operator += check_info[char]["min_count"]
        elif char in DIGITS:
            guarantee_taken += check_info[char]["min_count"]

    # Reduce max_count by guarantee_taken, and remove
    # all exact positions from possible positions
    for char in check_info:
        # Check if the number of char is fixed or not (include the case of "=")
        # If not, reduce max_count by guarantee_taken or guarantee_operator
        if check_info[char]["min_count"] != check_info[char]["max_count"]:
            if char in OPERATORS:
                check_info[char]["max_count"] -= (guarantee_operator - check_info[char]["min_count"])
            else:
                check_info[char]["max_count"] -= (guarantee_taken - check_info[char]["min_count"])
        if len(check_info[char]["exact_positions"]) == check_info[char]["max_count"]:
            check_info[char]["possible_positions"] = set()
        if len(check_info[char]["possible_positions"]) + len(check_info[char]["exact_positions"]) == \
            check_info[char]["min_count"]:
            check_info[char]["exact_positions"] |= \
                check_info[char]["possible_positions"]
            all_green |= check_info[char]["possible_positions"]
            check_info[char]["possible_positions"] = set()
        # Remove char with max_count == 0
        if check_info[char]["max_count"] == 0:
            valid_char.discard(char)
    
    # Prefill all other characters not mentioned in all_info with:
    # No exact positions, all possible postions (except exact), min_count = 0,
    # and max_count depends on whether it's a digit, operator or equal
    for char in POSSIBLE_CHAR:
        if char not in check_info:
            max_value = max_possible - guarantee_taken
            possible_postions = set(range(difficulty))
            if char in OPERATORS:
                max_value = 2 - guarantee_operator
                possible_postions = op_positions
            elif char == EQUALITY:
                max_value = 1
                possible_postions = equal_positions
            check_info[char] = \
                {"exact_positions": set(), 
                 "possible_positions": possible_postions - all_green, 
                 "min_count": 0, "max_count": max_value}

    # Remove all_green from possible
    for char in check_info:
        check_info[char]["possible_positions"] -= all_green
        remove = set()
        # Remove all invalid positions from the frequency table
        for positions in check_info[char]["possible_positions"]:
            if char not in FREQ_TABLE[difficulty][positions]:
                remove.add(positions)
        check_info[char]["possible_positions"] -= remove

    
    return(check_info, all_green, valid_char, valid_opp, op1_positions, op2_positions)

def check_if_valid(check_info, guess):
    ''' Checking if each char in guest info: 
    1) Has count between min_count and max_count, 
    2) Contains all the exact positions, 
    3) All other positions are in possible set '''
    guess_info = parse_info_unordered(guess)
    for char in check_info:
        if char in guess_info:
            positions = guess_info[char]
            exact_positions = check_info[char]["exact_positions"]
            possible_positions = check_info[char]["possible_positions"]
            min_count = check_info[char]["min_count"]
            max_count = check_info[char]["max_count"]
            if not(min_count <= len(positions) <= max_count):
                # print(char, "count", check_info[char])
                return(False)
            if (exact_positions & positions) != exact_positions:
                # print(char, "exact", check_info[char])
                return(False)
            remain = positions - exact_positions
            if (possible_positions & remain) != remain:
                # print(char, "possible", check_info[char])
                return(False)
        else:
            if check_info[char]["min_count"] != 0:
                # print(char, "missing", check_info[char])
                return(False)
    return(True)

def sort_char(prefill_guess, difficulty, check_info):
    '''
    Sort the character by its frequency and a preference toward unchecked char
    '''
    curr_freq = FREQ_TABLE[difficulty]
    priority_guess = [None for i in range(len(prefill_guess))]
    for position in range(len(prefill_guess)):
        curr_freq_post = curr_freq[position]
        sorted_char = sorted(prefill_guess[position],
                    key=lambda char: 3 * curr_freq_post[char] - 
                    (len(check_info[char]["possible_positions"]) - 
                     check_info[char]["min_count"])/max(len(check_info[char]["possible_positions"]), 1),
                    reverse=True)
        prefill_guess[position] = sorted_char
        priority_guess[position] = sorted_char[:3]
    return(prefill_guess, priority_guess)

def calc_prop(guess):
    " Find total propability of a guess"
    total_prop = 10
    difficulty = len(guess)
    for i in range(difficulty):
        total_prop *= FREQ_TABLE[difficulty][i][guess[i]] * 10
    return(total_prop)

def find_valid_guess(check_info, operators_combination):
    '''
    Receive the combinations of possible guesses with the operators placed in valid position.
    Proceed with the checking for valid with `all_info` and mathematical correctness.
    Return the guess with a valid_score: 0 - purely random; 1 - pass all_info check; 
    2 - pass mathematical check (valid guess)
    '''
    valid = set()
    valid_score = 0
    max_check = max_valid = 200
    sequence = ""
    for equal_post in operators_combination:
        for guess in operators_combination[equal_post]:
            all_combinations = product(*guess)
            count = 0
            for combination in all_combinations:
                sequence = "".join(combination)
                count += 1
                check = check_if_valid(check_info, sequence)
                if check:
                    equation = sequence[:equal_post]
                    result = sequence[(equal_post + 1):]
                    valid.add((equation, result))
                if count > max_check:
                    break
    if len(valid) == 0:
        return(sequence, valid_score)
    valid_score = 1
    count = 0
    max_correct = ""
    max_correct_prob = 0
    max_incorrect = "" #  Valid, but incorrect seq
    max_incorrect_prob = 0
    for valid_tup in valid:
        count += 1
        try:
            curr_guess = valid_tup[0] + "=" + valid_tup[1]
            curr_prop = calc_prop(curr_guess)
            if curr_prop > max_incorrect_prob:
                    max_incorrect = curr_guess
                    max_incorrect_prob = curr_prop
            if eval(valid_tup[0]) == int(valid_tup[1]):
                valid_score = 2
                if curr_prop > max_correct_prob:
                    max_correct = curr_guess
                    max_correct_prob = curr_prop
                
        except (SyntaxError, ZeroDivisionError) as e:
            # print("Error", e)
            pass
        if count > max_valid:
            break
    if max_correct:
        return(max_correct, valid_score)
    return(max_incorrect, valid_score)


# Character wise approach:
def create_better_guess(all_info, difficulty=DEF_DIFFIC):
    '''
    Takes information built up from past guesses that is stored in `all_info`, 
    and uses it as guidance to generate a new guess of length `difficulty`. 
    Use 2 first guesses for exploration, and the other guesses are enforced to be
    in the format. 
    1st guess: Guarantee operators val and equal position;
    2nd guess: Check as much uncheck digits as possible;
    3rd+ guess: Form an iter of combinations of possible val with 
    operators in the correct position;
    then search within these combination for a valid guess (
    pass `all_info` check and mathematically correct)
    '''

    curr_freq = FREQ_TABLE[difficulty]

    # Initial guess - Cover as much char and operator as possible
    # Guarantee identify the operators and equal positions
    if all_info == []:
        return(FIRST_GUESS[difficulty])
    elif len(all_info) == 1:
        # Try to rank char by its "uncertainty" and place it in the guess
        check_info, all_green, valid_char, valid_opp, check_op1, check_op2 = parse_all_info(all_info, difficulty)
        guess = ""
        score = {}
        for char in valid_char:
            if char != EQUALITY and char != OPERATORS:
                score[char] = (len(check_info[char]["possible_positions"]) - check_info[char]["min_count"] - 10000 * len(check_info[char]["exact_positions"]))/max(len(check_info[char]["possible_positions"]), 1)
        for i in range(difficulty):
            check_char = "9"
            max_score = -10**6
            for char in curr_freq[i].keys():
                if char in valid_char and char != EQUALITY and char not in guess and char != OPERATORS:
                    curr_score = (3 * score[char] + curr_freq[i][char])
                    if curr_score > max_score:
                        check_char = char
                        max_score = curr_score
            guess += check_char
        return(guess)
    else:
        check_info, all_green, valid_char, valid_opp, check_op1, check_op2 = parse_all_info(all_info, difficulty)
        
        # Initialize possible positions of op1 and op2 as guaranteed by first guess
        num_opp = len(valid_opp)
        if num_opp == 1:
            op1 = op2 = tuple(valid_opp)[0]
        else:
            op1, op2 = tuple(valid_opp)

        # Prefill guess with possible and exact positions
        prefill_guess = [set() for i in range(difficulty)]
        op1_exact = False
        op2_exact = False
        for char in valid_char:
            exact_positions = check_info[char]["exact_positions"]
            for exact_post in exact_positions:
                prefill_guess[exact_post].add(char)
                if char in OPERATORS:
                    if exact_post in check_op1:
                        op1_positions = {exact_post}
                        op1_exact = True
                        if num_opp == 2:
                            op1 = char
                            op2 = tuple((x for x in valid_opp if x != op1))[0]
                    else:
                        op2_positions = {exact_post}
                        op2_exact = True
                        if num_opp == 2:
                            op2 = char
                            op1 = tuple((x for x in valid_opp if x != op2))[0]
            if char not in OPERATORS and char != EQUALITY:
                for possible_post in check_info[char]["possible_positions"]:
                    prefill_guess[possible_post].add(char)
        
        # Sort the prefill_guess by its probability (and a bit of preference for unchecked char)
        # prefill_guess: Convert to 2D list
        prefill_guess, priority_guess = sort_char(prefill_guess, difficulty, check_info)

        if not op1_exact:
            op1_positions = check_info[op1]["possible_positions"]
        if not op2_exact:
            op2_positions = check_info[op2]["possible_positions"]
        
        # Guarantee positions of equal sign
        equal_positions = set()
        if check_info[EQUALITY]["exact_positions"]:
            equal_positions = check_info[EQUALITY]["exact_positions"]
        else:
            equal_positions = check_info[EQUALITY]["possible_positions"]
        

        # Form all valid combinations with operators placed in correct position
        # operators_combination (dict): Store all such valid combinations with
        # operators: Key = the equal positions sign, Value = 2d_tuple storing
        # all possible values at position = index of outer tuple.
        operators_combination = {}
        priority_combination = {} 
        for op1_post in op1_positions:
            for op2_post in op2_positions:
                for equal_post in equal_positions:
                    if 2 <= abs(op2_post - op1_post) <= 3 and \
                        ((2 <= (equal_post - op2_post) <= 3 and op2_post > op1_post) or \
                        (2 <= (equal_post - op1_post) <= 3 and op1_post > op2_post)) and \
                        (op2_exact or op2_post not in all_green) and \
                        (op1_exact or op1_post not in all_green):
                         new_guess = copy.deepcopy(prefill_guess)
                         new_priority_guess = copy.deepcopy(priority_guess)
                         new_guess[op1_post] = new_priority_guess[op1_post] = [op1]
                         new_guess[op2_post] = new_priority_guess[op2_post] = [op2]
                         new_guess[equal_post] = new_priority_guess[equal_post] = [EQUALITY]
                         if equal_post in operators_combination:
                            operators_combination[equal_post].append(new_guess)
                         else:
                            operators_combination[equal_post] = [new_guess]
                         if equal_post in priority_combination:
                            priority_combination[equal_post].append(new_priority_guess)
                         else:
                            priority_combination[equal_post] = [new_priority_guess]
        

        priority_guess, valid_priority = find_valid_guess(check_info, priority_combination)

        if valid_priority == 2:
            return(priority_guess) 
        rest_guess, valid_rest = find_valid_guess(check_info, operators_combination)

        if valid_rest > valid_priority:
            return(rest_guess)
        return(priority_guess)