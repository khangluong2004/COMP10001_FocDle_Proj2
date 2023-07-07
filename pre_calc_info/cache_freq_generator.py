import json
from itertools import product
from collections import defaultdict
operators = ("+", "-", "*", "%")
values = list(map(str, range(1, 100)))
total_table = {}
count_table = {}


all_express = list(map(lambda x: "".join(x), product(values, operators, values, operators, values)))
for express in all_express:
    result = eval(express)
    if result > 0:
        guess = express + "=" + str(result)
        difficulty = len(guess)
        if difficulty not in count_table:
            count_table[difficulty] = {}
        if difficulty not in total_table:
            total_table[difficulty] = defaultdict(int)
        curr_count = count_table[difficulty]
        curr_total = total_table[difficulty]
        for i in range(difficulty):
            if i not in curr_count:
                curr_count[i] = defaultdict(int)
            curr_count[i][guess[i]] += 1
            curr_total[i] += 1

for diff in count_table:
    for pos in count_table[diff]:
        for val in count_table[diff][pos]:
            count_table[diff][pos][val] /= total_table[diff][pos]

with open("freq_table.json", "w") as file:
    json.dump(count_table, file)
