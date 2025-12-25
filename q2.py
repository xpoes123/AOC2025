from aoc_utils import submit_answer, submit_answer2, get_input

DAY = 2
LINES = get_input(DAY, delim=",")

@submit_answer(day=DAY)
def solve_1() -> str:
    total = 0
    for line in LINES:
        id_low, id_high = line.split("-")
        for i in range(int(id_low), int(id_high)+1):
            s = str(i)
            if len(s) % 2 == 1:
                continue
            first_half = s[:len(s)//2]
            if s == first_half * 2:
                total += i
    print(total)
    return str(total)

@submit_answer2(day=DAY)
def solve_2() -> str:
    total = 0
    for line in LINES:
        id_low, id_high = line.split("-")
        for i in range(int(id_low), int(id_high)+1):
            s = str(i)
            len_s = len(s)
            factors = []
            for j in range(1, len_s):
                if len_s % j == 0:
                    factors.append(j)
            for factor in factors:
                first_part = s[:factor]
                if s == first_part * (len_s//factor):
                    total += i
                    print(i, factor, id_low, id_high)
                    break
    return str(total)

# solve_1()
solve_2()