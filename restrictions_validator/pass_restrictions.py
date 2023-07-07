# A more complete version of restrictions used for improved 
# guess accuracy.

# The same algorithms are incorp. directly inside guess_makers to generate
# guess that should pass the restrictions. 
# The methods specified here are only used for the simple guess mechanism.

GREEN = "green"
YELLOW = "yellow"
GREY = "grey"
OPERATORS = "+-*%"
DIGITS = "0123456789"
EQUALITY = "="
POSSIBLE_CHAR = OPERATORS + EQUALITY + DIGITS

def parse_info_unordered(phrase):
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

def passes_restrictions(guess, all_info):
    '''
    Tests a `guess` equation against `all_info`, a list of known restrictions, 
    one entry in that list from each previous call to set_colors(). Returns 
    True if that `guess` complies with the collective evidence imposed by 
    `all_info`; returns False if any violation is detected. Does not check the 
    mathematical accuracy of the proposed candidate equation.
    '''
    # guess_info: Dictionary with key=char, value=positions: set
    # check_info: Dictionary with key=char, 
    # value={exact_positions: set, possible_positions: set, 
    # min_count: int, max_count: int}
    all_values = set(range(len(guess)))
    # op1, op2, equal positions derived from the fact that 
    # each value must have 1-2 digits, and the final result
    # has at least 1 digit
    # op1_positions = {x for x in (1, 2) if x <= len(guess) - 6}
    # op2_positions = {x for x in (3, 4, 5) if x <= len(guess) - 4}
    # op_positions = op1_positions | op2_positions
    # equal_positions = {x for x in (5, 6, 7, 8) if x <= len(guess) - 2} 
    max_possible = len(guess) - 3
    guess_info = parse_info_unordered(guess)
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
                possible_positions = all_values
                # if curr_char in OPERATORS:
                #     max_value = 2
                #     possible_positions = op_positions
                # elif curr_char == EQUALITY:
                #     max_value = 1
                #     possible_positions = equal_positions
                if curr_color == GREEN:
                    sublist_info[curr_char] = \
                        {"exact_positions": {curr_position}, 
                         "possible_positions": 
                            possible_positions - {curr_position}, 
                         "min_count": 1, "max_count": max_value}
                    all_green.add(curr_position)
                elif curr_color == YELLOW:
                    sublist_info[curr_char] = \
                        {"exact_positions": set(), 
                         "possible_positions": 
                            possible_positions - {curr_position}, 
                         "min_count": 1, "max_count": max_value}
                else:
                    sublist_info[curr_char] = {"exact_positions": set(), 
                                               "possible_positions": set(), 
                                               "min_count": 0, "max_count": 0}
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
        # print(sublist_info["2"], "SUBLIST")
        # print(check_info["2"], "CHECK_INFO")
    
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
                check_info[char]["max_count"] -= \
                    (guarantee_operator - check_info[char]["min_count"])
            else:
                check_info[char]["max_count"] -= \
                    (guarantee_taken - check_info[char]["min_count"])
        exact_num = len(check_info[char]["exact_positions"])
        if exact_num == check_info[char]["max_count"]:
            check_info[char]["possible_positions"] = set()
        if len(check_info[char]["possible_positions"]) + exact_num == \
            check_info[char]["min_count"]:
            check_info[char]["exact_positions"] |= \
                check_info[char]["possible_positions"]
            all_green |= check_info[char]["possible_positions"]
            check_info[char]["possible_positions"] = set()
    for char in check_info:
        check_info[char]["possible_positions"] -= all_green
    
    # Prefill all other characters not mentioned in all_info with:
    # No exact positions, all possible postions (except exact), min_count = 0,
    # and max_count depends on whether it's a digit, operator or equal
    for char in POSSIBLE_CHAR:
        if char not in check_info:
            max_value = max_possible
            possible_postions = set(range(len(guess)))
            # if char in OPERATORS:
            #     max_value = 2
            #     possible_postions = op_positions
            # elif char == EQUALITY:
            #     max_value = 1
            #     possible_postions = equal_positions
            check_info[char] = \
                {"exact_positions": set(), 
                 "possible_positions": possible_postions, 
                 "min_count": 0, "max_count": max_value}

    # Checking if each char in guest info: 
    # 1) Has count between min_count and max_count, 
    # 2) Contains all the exact positions, 
    # 3) All other positions are in possible set
    for char in check_info:
        if char in guess_info:
            positions = guess_info[char]
            exact_positions = check_info[char]["exact_positions"]
            possible_positions = check_info[char]["possible_positions"]
            min_count = check_info[char]["min_count"]
            max_count = check_info[char]["max_count"]
            if not(min_count <= len(positions) <= max_count):
                print(char, "count", check_info[char])
                return(False)
            if (exact_positions & positions) != exact_positions:
                print(char, "exact", check_info[char])
                return(False)
            remain = positions - exact_positions
            if (possible_positions & remain) != remain:
                print(char, "possible", check_info[char])
                return(False)
        else:
            if check_info[char]["min_count"] != 0:
                print(char, "missing", check_info[char])
                return(False)
    return(True)