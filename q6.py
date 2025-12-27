from aoc_utils import (
    submit_answer,
    submit_answer2,
    get_input,
    int_arr_to_int,
    int_to_arr,
)

DAY = 6
LINES = get_input(DAY)


@submit_answer(day=DAY, debug=True)
def solve_1():
    lines = []
    # print(LINES)
    for line in LINES:
        lines.append(line.split())
    lines = [[row[i] for row in lines] for i in range(len(lines[0]))]
    for line in lines:
        op = line[-1]
        vals = list(map(int, line[:-1]))

    return ""


@submit_answer2(day=DAY, debug=True)
def solve_2():
    return ""


solve_1()
# solve_2()
