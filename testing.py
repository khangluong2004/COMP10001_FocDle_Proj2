import random
import json
import time
from collections import defaultdict
from guess_makers.better_guess_v2 import create_better_guess
from project2_helper_functions import set_colors, create_secret

GREEN = "green"
YELLOW = "yellow"
GREY = "grey"
DEF_DIFFIC = 10
OPERATORS = "+-*%"
EQUALITY = "="
DIGITS = "0123456789"

# Testing

def all_green(info):
    '''
    Return True if all the colors in `info` are green, False otherwise.
    '''
    return all(color == GREEN for _, _, color in info)

def solve_FoCdle(secret):
    '''
    For a given `secret` equation, play out a game of FoCdle, returning a tuple
    of the number of guesses required to find the secret, and the secret itself.
    Note that we aren't allowed to look at the value of `secret` directly -- it
    is only taken as a parameter for the sake of `set_colors()`, and to infer
    the respective difficulty. Most importantly, `create_guess()` cannot see it!
    '''
    difficulty = len(secret)

    # each element of `all_info` will be a list of tuples returned by
    # `set_colors`, the function you wrote in task 2
    all_info = []
    nguesses = 0

    for i in range(20):
        # iterate a controlled number of times to try and find a guess that
        # complies with the information that has been built up

        new_guess = create_better_guess(all_info, difficulty)
        # print("ACTUAL GUESS: ", new_guess)
        # for better or worse, now apply that latest guess
        new_info = set_colors(secret, new_guess)
        nguesses += 1
        if all_green(new_info):
            # wow, we have the answer, party time
            return (nguesses, new_guess)
        else:
            # didn't hit the solution, but hopefully will get additional
            # information to use when generating next candidate
            all_info.append(new_info)
    return(nguesses, new_guess)


# finally we're ready to play a game of FoCdle...
avg_correct = 0
max_corr = 0
min_corr = 10000
avg_count = 0
error = 0
max_guess = 0
results = defaultdict(int)
start = time.time()

TEST_CASES = 10000

for i in range(TEST_CASES):
    difficulty = random.randint(7, 15)
    secret = create_secret(difficulty)
    if secret == "No FoCdle found of that difficulty":
        continue
    print("SECRET:", secret)
    nguesses, final_guess = solve_FoCdle(secret)
    if final_guess == secret:
        results[nguesses] += 1
        if nguesses < min_corr:
            min_corr = nguesses
        if nguesses > max_corr:
            max_corr = nguesses
        avg_correct += nguesses
        avg_count += 1
        if nguesses > max_guess:
            max_guess = nguesses
    else:
        print("ERROR:", final_guess, secret)
        error += 1

print("----------------------")
print("Time per guess:", (time.time() - start) / TEST_CASES)
print(f"Error count: {error}")
print(f"Average guess of {avg_correct/ avg_count} for {avg_count} secrets")
print(f"Max: {max_corr}")
print(f"Min: {min_corr}")