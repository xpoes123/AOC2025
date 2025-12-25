import requests
import os
from dotenv import load_dotenv
from collections.abc import Callable
import time

load_dotenv()

def get_input(day: int, delim: str="\n") -> list[str]:
    session = os.getenv("SESSION")
    if not isinstance(session, str):
        raise ValueError("SESSION environment variable not set")
    return requests.get(
        f"https://adventofcode.com/2025/day/{day}/input",
        cookies={
            "session": session
        },
    ).text.split(delim)


def submit_answer(*, day: int, debug: bool = False) -> Callable[[Callable[[], str]], Callable[[], str]]:
    def decorator(ans_fn: Callable[[], str]) -> Callable[[], str]:
        def wrapped() -> str:
            answer = ans_fn()
            session = os.getenv("SESSION")
            if not isinstance(session, str):
                raise ValueError("SESSION environment variable not set")
            if not debug:
                resp = requests.post(
                    f"https://adventofcode.com/2025/day/{day}/answer",
                    cookies={"session": session},
                    data={"level": str(1), "answer": answer},
                )
                print(resp.text)
            else:
                print(answer)
            return answer
        return wrapped
    return decorator


def submit_answer2(*, day: int, debug: bool = False) -> Callable[[Callable[[], str]], Callable[[], str]]:
    def decorator(ans_fn: Callable[[], str]) -> Callable[[], str]:
        def wrapped() -> str:
            answer = ans_fn()

            session = os.getenv("SESSION")
            if not isinstance(session, str):
                raise ValueError("SESSION environment variable not set")
            if not debug:
                resp = requests.post(
                    f"https://adventofcode.com/2025/day/{day}/answer",
                    cookies={"session": session},
                    data={"level": str(2), "answer": answer},
                )
                print(resp.text)
            else:
                print(answer)
            return answer
        return wrapped
    return decorator