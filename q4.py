from aoc_utils import (
    submit_answer,
    submit_answer2,
    get_input,
    int_arr_to_int,
    int_to_arr,
)

DAY = 4
LINES = get_input(DAY)

DIRECTIONS = {(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)}


@submit_answer(day=DAY, debug=True)
def solve_1():
    tot = 0
    for idx, line in enumerate(LINES):
        for jdx, char in enumerate(line):
            if char != "@":
                continue
            count = 0
            for dir in DIRECTIONS:
                didx = idx + dir[0]
                djdx = jdx + dir[1]
                if didx < 0 or djdx < 0 or didx == len(LINES) or djdx == len(line):
                    continue
                if LINES[didx][djdx] == "@":
                    count += 1
            if count < 4:
                tot += 1
    return tot


@submit_answer2(day=DAY)
def solve_2():
    tot = 0
    idx_set = set()
    lines = [list(line) for line in LINES]
    iter = 0
    while True:
        iter += 1
        for idx, line in enumerate(lines):
            for jdx, char in enumerate(line):
                if char != "@":
                    continue
                count = 0
                for dir in DIRECTIONS:
                    didx = idx + dir[0]
                    djdx = jdx + dir[1]
                    if didx < 0 or djdx < 0 or didx == len(LINES) or djdx == len(line):
                        continue
                    if lines[didx][djdx] == "@":
                        count += 1
                if count < 4:
                    idx_set.add((idx, jdx))
        if len(idx_set) == 0:
            break
        tot += len(idx_set)
        for cord in idx_set:
            # print(lines[cord[0]][cord[1]])
            lines[cord[0]][cord[1]] = "."
            idx_set = set()
    print(iter)
    return tot


solve_1()
solve_2()
