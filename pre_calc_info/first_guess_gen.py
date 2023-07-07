import json
import itertools
from freq_result import FREQ_TABLE
from collections import defaultdict

GREEN = "green"
YELLOW = "yellow"
GREY = "grey"
DEF_DIFFIC = 10
OPERATORS = "+-*%"
EQUALITY = "="
DIGITS = "0123456789"
POSSIBLE_CHAR = OPERATORS + EQUALITY + DIGITS

def check_op(phrase):
    for char in OPERATORS:
        if char not in phrase:
            return(False)
    return(True)

operator_post = {}
for diff in FREQ_TABLE:
    operator_post[diff] = []
    all_post = tuple(range(diff))
    for a in all_post:
        for b in all_post:
            for c in all_post:
                for d in all_post:
                    if a not in (b, c, d) and b not in (a, c, d) and c not in (b, a, d) and d not in (a, c, b):
                        operator_post[diff].append((a, b, c, d))



best_guess = {}
for diff in FREQ_TABLE:
    curr_opp_post = operator_post[diff]
    curr_table = FREQ_TABLE[diff]
    max_seq = ""
    maximum_prob = -1
    for opp_post in curr_opp_post:
        seq = ""
        seq_prob = 100
        for post in curr_table:
            max_prob = 0
            if "=" in curr_table[post]:
                max_char = "="
                max_prob = curr_table[post][max_char]
            elif post in opp_post:
                max_char = OPERATORS[opp_post.index(post)]
                if max_char not in curr_table[post]:
                    max_prob = 0.00001
                else:
                    max_prob = curr_table[post][max_char]
            else:
                try:
                    max_char = max(filter(lambda x: x in DIGITS, curr_table[post].keys()), key= lambda x: curr_table[post][x])
                    max_prob = curr_table[post][max_char]
                except ValueError:
                    seq = "$"
                    break
            if max_char in DIGITS and max_char in seq:
                max_prob /= 10**(diff//2)
            seq += max_char
            seq_prob *= max_prob * 10
        if seq != "$" and seq_prob > maximum_prob and check_op(seq):
            maximum_prob = seq_prob
            max_seq = seq
    best_guess[diff] = max_seq
print(best_guess)

with open("fguess.json", "a") as fp:
    json.dump(best_guess, fp)           

