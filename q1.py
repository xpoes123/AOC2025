from aoc_utils import submit_answer, submit_answer2, get_input

YEAR = 2025
DAY = 1
LINES = get_input(DAY)


@submit_answer(day=DAY, debug=False)
def solve_1() -> str:
    point = 50
    total = 0
    for line in LINES:
        if len(line) == 0:
            break
        direction, magnitude = line[0], int(line[1:])
        if direction == "R":
            point = (point + magnitude) % 100
        else:
            point = (point - magnitude) % 100
        if point == 0:
            total += 1
    return str(total)

@submit_answer2(day=DAY)
def solve_2() -> str:
    point = 50
    total = 0
    for line in LINES:
        if len(line) == 0:
            break
        direction, magnitude = line[0], int(line[1:])
        if direction == "R":
            raw_point = point + magnitude
            total += raw_point // 100
            point = (point + magnitude) % 100
        else:
            raw_point = (100-point) + magnitude
            total += raw_point // 100
            if point == 0:
                total -= 1
            point = (point - magnitude) % 100
        # print(total, point, magnitude, direction)
    return str(total)


# solve_1()
solve_2()