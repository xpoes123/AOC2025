from aoc_utils import (
    submit_answer,
    submit_answer2,
    get_input,
    int_to_arr,
    int_arr_to_int,
)

DAY = 3
LINES = get_input(DAY)


@submit_answer(day=DAY)
def solve_1():
    sum = 0
    for line in LINES:
        if len(line) == 0:
            break
        s = int_to_arr(line)
        m = max(s)
        start_idx = s.index(m)
        if len(s[start_idx + 1 :]) > 0:
            m2 = max(s[start_idx + 1 :])
            sum += m * 10 + m2
        else:
            m2 = max(s[:start_idx])
            sum += 10 * m2 + m
    return sum


# Idea here is you want to find the largest digit and then the largest string you can make after that
# This gives you n digits, and then you repeat on the largest digit before the largest digit and so on until you hit 12


# 171419245422055
@submit_answer2(day=DAY, debug=True)
def solve_2():
    tot = 0
    for line in LINES:
        tot += int_arr_to_int(best_subseq_len_L(int_to_arr(line), 12))
    return tot


def best_subseq_len_L(s: list[int], L: int) -> list[int]:
    n = len(s)
    if L <= 0:
        return []
    if n == L:
        return s[:]

    k = n - L

    window = s[: k + 1]
    m = max(window)
    i = window.index(m)

    return [m] + best_subseq_len_L(s[i + 1 :], L - 1)


@submit_answer2(day=DAY, debug=True)
def solve_2_stack():
    tot = 0
    for line in LINES:
        ns = int_to_arr(line)
        stack = []
        k = len(ns) - 12
        for n in ns:
            while k > 0 and stack and stack[-1] < n:
                stack.pop()
                k -= 1
            stack.append(n)

        if k > 0:
            stack = stack[:-k]
        tot += int_arr_to_int(stack)
    return tot


# 6563436486136355463655575366345554384456562545629262586425424652243626548657625466455656653543945665

# solve_1()
# solve_2()
solve_2_stack()
