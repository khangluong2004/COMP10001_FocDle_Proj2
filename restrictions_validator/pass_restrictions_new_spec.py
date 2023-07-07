GREEN = "green"
# Fully documented & followed the assignments' specifications
# for checking if a guess is valid. 
# The specifications are not completed. See improved version in pass_restrictions

YELLOW = "yellow"
GREY = "grey"
OPERATORS = "+-*%"
DIGITS = "0123456789"
EQUALITY = "="
POSSIBLE_CHAR = OPERATORS + EQUALITY + DIGITS


def initial_info(curr_color: str, curr_position: int, 
                 all_green: set, all_positions: set, total_grey: int) -> tuple:
    '''
    Initialize information of each char based on its color in
    its first appearance sublist of all_info. 
    Return the 2-tuple: total_grey: int, initial_val: dict.
    Mutate the all_green set.
    '''
    initial_val = {}
    if curr_color == GREEN:
        initial_val= {"exact_positions": {curr_position}, 
                      "possible_positions": all_positions - {curr_position}, 
                      "min_count": 1, "max_count": len(all_positions)}
        all_green.add(curr_position)

    elif curr_color == YELLOW:
        initial_val = {"exact_positions": set(), 
                       "possible_positions": all_positions - {curr_position}, 
                       "min_count": 1, "max_count": len(all_positions)}  
    else: #  Last case: GREY
        total_grey += 1
        initial_val = {"exact_positions": set(), 
                        "possible_positions": set(), 
                        "min_count": 0, "max_count": 0}
    return(total_grey, initial_val)

def update_info(curr_entry: dict, curr_color: str, 
                curr_position: int, total_grey: int, all_green: set) -> int:
    '''
    Update info of each char in check_info in the 2nd (or more) appearances
    based on their color. 
    Mutate curr_entry and Return the updated total_grey count.
    '''
    if curr_color == GREEN:
        curr_entry["exact_positions"].add(curr_position)
        curr_entry["possible_positions"].discard(curr_position)
        # If encountered a grey before (recognize by max = min), 
        # increment both max_count and min_count
        # to ensure max_count include the current GREEN 
        if curr_entry["max_count"] == curr_entry["min_count"]:
            curr_entry["max_count"] += 1
        curr_entry["min_count"] += 1
        all_green.add(curr_position)
    elif curr_color == YELLOW:
        curr_entry["possible_positions"].discard(curr_position)
        curr_entry["min_count"] += 1
    else: #  Last case: GREY
        total_grey += 1
        curr_entry["possible_positions"].discard(curr_position)
        # Make max_count equal to num of green and yellow
        # appearances of curr_char (stored in min_count)
        curr_entry["max_count"] = curr_entry["min_count"]
    return(total_grey)

def parse_sublist_info(sublist: list, difficulty: int) -> tuple:
    '''
    Extract all position/ count info from `sublist` and return all key infos  
    in 4-tuple (`total_grey`, `all_green`, `all_positions`, `check_info`).

    Return data details:
    1. `total_grey`: int, storing the total "grey" tags in sublist
        Used to calculate the upper bound for each characters:
        Max_count = Number_green_yellow_of_that_char + total_grey
    2. `all_green`: set, storing positions where green positions're found
        Used to remove those positions from possible positions for each char
    3. `all_positions`: set, all possible values at the current point.
        Used for initialisation.
    4. `check_info`: dict of dict, with key=char, 
        value={exact_positions: set, possible_positions: set, 
        min_count: int, max_count: int}
        Storing info for each char from sublist of all_info
    '''
    # Variables described in "Return data details" above
    all_positions = set(range(difficulty))
    all_green = set()
    total_grey = 0
    # sublist_info: Dictionary with key=char, value={exact_positions: set, 
    # possible_positions: set, min_count: int, max_count: int}
    # min_count: Number of green and yellow postions
    # max_count: Initialize as `difficulty`, and  
    #   change to = min_count, if a grey is detected
    check_info = {}
    for char_info in sublist:
        curr_position, curr_char, curr_color = char_info
        if curr_char not in check_info:
            # Initialisation (and update all_green)
            total_grey, check_info[curr_char] = \
                initial_info(curr_color, curr_position, 
                                all_green, all_positions, total_grey)
        else:
            curr_entry = check_info[curr_char]
            total_grey = update_info(curr_entry, curr_color, 
                                        curr_position, total_grey, all_green)  
    return(total_grey, all_green, all_positions, check_info)


def post_refine_check_info(check_info: dict, total_grey: int, 
                           all_green: set, all_positions: set) -> tuple:
    '''
    Receive check_info, total_grey, all_green, all_positions
    (values stored in each arguments is noted in parse_sublist_info), 
    then:
    1. For all char which hasn't detected a grey, update the max count:
        max_count = min_count (Store number of yellow/green) + total_grey
    2. Remove all all_green (green char) positions from possible_positions
        (non-exact positions) for all char and `all_positions` 
        (for initialisation);
    Return the updated all_positions and check_info    
    '''
    # Update max count (1.)
    for char in check_info:
        # Check if the number of char is fixed or not (find a grey or not)
        # If not, change to min_count + total_grey
        if check_info[char]["min_count"] != check_info[char]["max_count"]:
            check_info[char]["max_count"] = \
                check_info[char]["min_count"] + total_grey 

    # Remove all_green positions (2.)
    for char in check_info:
        check_info[char]["possible_positions"] -= all_green
    all_positions -= all_green
    return(all_positions, check_info)

def prefill_char(check_info: dict, total_grey: int, 
                 all_positions: set) -> dict:
    '''
    Receive check_info, total_grey, all_positions 
    (arguments explained in parse_sublist_info function)
    Prefill all other characters not mentioned in sublist with:
    No exact positions, all possible postions (except exact), min_count = 0,
    and max_count = total_grey
    Return the updated check_info
    '''
    for char in POSSIBLE_CHAR:
        if char not in check_info:
            check_info[char] = {"exact_positions": set(), 
                                "possible_positions": all_positions, 
                                "min_count": 0, "max_count": total_grey}
    return(check_info)

def parse_info_unordered(phrase: str) -> dict:
    ''' 
    Receive the `phrase` as argument, and return a chars_info dictionary 
    with key = character and value=positions: set of positions of that
    character

    Arguments:
    Phrase -- str: A guess in this context
    '''
    chars_info = {}
    # Fill the chars_info for each char in secret
    for i in range(len(phrase)):
        if phrase[i] in chars_info:
            chars_info[phrase[i]].add(i)
        else:
            chars_info[phrase[i]] = {i}
    return(chars_info)

def passes_restrictions(guess: str, all_info: list) -> bool:
    '''
    Tests a `guess` equation against `all_info`, a list of known restrictions, 
    one entry in that list from each previous call to set_colors(). 
    Returns True if that `guess` complies with the collective evidence imposed 
    by `all_info`; returns False if any violation is detected. Does not check  
    the mathematical accuracy of the proposed candidate equation.
    '''

    # Extract the locations of each char from the guess:
    # guess_info: Dictionary with key=char, value=positions: set
    guess_info = parse_info_unordered(guess)

    for sublist in all_info:
        # Extract info from sublist
        total_grey, all_green, all_positions, check_info =\
            parse_sublist_info(sublist, len(guess))
        # Refine the info (remove all_green and update max_count)
        all_positions, check_info = \
            post_refine_check_info(check_info, total_grey, all_green, 
                                   all_positions)
        # Prefill info for all chars that haven't appeared in sublist
        check_info = prefill_char(check_info, total_grey, all_positions)


        # Checking if each char in guest info: 
        # 1. Has count between min_count and max_count, 
        # 2. Contains all the exact positions, 
        # 3. All other positions are in possible set
        for char in check_info:
            if char in guess_info:
                positions = guess_info[char]
                exact_positions = check_info[char]["exact_positions"]
                possible_positions = check_info[char]["possible_positions"]
                min_count = check_info[char]["min_count"]
                max_count = check_info[char]["max_count"]
                # Check the Distributional constraints
                if not(min_count <= len(positions) <= max_count):
                    print("Count", char, check_info[char])
                    return(False)
                # Check if the guess contains all the MUST-have exact
                # positions (where green char is detected)
                if (exact_positions & positions) != exact_positions:
                    print("Exact", char, check_info[char])
                    return(False)
                # Check if non-exact positions are in the possible positions
                # from check_info
                remain = positions - exact_positions
                if (possible_positions & remain) != remain:
                    print("Possible", char, check_info[char])
                    return(False)
            else:
                # If a char has a min_count of 1 in check_info,
                # but doesn't appear in guess_info, then
                # Distributional constraints is violated
                if check_info[char]["min_count"] != 0:
                    print("Missing", char, check_info[char])
                    return(False)
    return(True)

