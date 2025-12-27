from aoc_utils import (
    submit_answer,
    submit_answer2,
    get_input,
    int_arr_to_int,
    int_to_arr,
)

DAY = 5
LINES = get_input(DAY)


@submit_answer(day=DAY, debug=False)
def solve_1():
    val_idx = -1
    s = 0
    ranges = []
    for idx, line in enumerate(LINES):
        if line == "":
            val_idx = idx
            break
        left, right = map(int, line.split("-"))
        ranges.append((left, right))
    ranges = sorted(ranges, key=lambda x: (x[0], x[1]))
    real_ranges = []
    left = 0
    right = 0
    for range in ranges:
        x, y = range
        if x > right:
            real_ranges.append((left, right))
            left = x
        right = max(right, y)
    real_ranges.append((left, right))
    for line in LINES[val_idx + 1 :]:
        if line == "":
            break
        for range in real_ranges:
            x, y = range
            if x <= int(line) <= y:
                s += 1
    return s


@submit_answer2(day=DAY, debug=False)
def solve_2():
    s = 0
    ranges = []
    for idx, line in enumerate(LINES):
        if line == "":
            break
        left, right = map(int, line.split("-"))
        ranges.append((left, right))
    ranges = sorted(ranges, key=lambda x: (x[0], x[1]))
    real_ranges = []
    left = 0
    right = 0
    for range in ranges:
        x, y = range
        if x > right:
            if right != 0:
                real_ranges.append((left, right))
            left = x
        right = max(right, y)
    real_ranges.append((left, right))
    for range in real_ranges:
        s += range[1] - range[0] + 1
    return s


# solve_1()
solve_2()
