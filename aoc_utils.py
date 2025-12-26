from __future__ import annotations

import os
import re
from dataclasses import dataclass
from functools import lru_cache, wraps
from typing import Callable, Literal, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

AOC_YEAR = 2025
AOC_BASE = f"https://adventofcode.com/{AOC_YEAR}"


def _require_session() -> str:
    session = os.getenv("SESSION")
    if not isinstance(session, str) or not session.strip():
        raise ValueError(
            "SESSION environment variable not set (expected AoC session cookie value)"
        )
    return session.strip()


@lru_cache(maxsize=1)
def _http() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": "aoc-helper/1.0 (github.com/you; contact: you@example.com)",
        }
    )
    s.cookies.set("session", _require_session())
    return s


_ARTICLE_RE = re.compile(
    r"<article[^>]*>(?P<body>.*?)</article>", re.DOTALL | re.IGNORECASE
)
_P_RE = re.compile(r"<p[^>]*>(?P<p>.*?)</p>", re.DOTALL | re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")


def _html_article_paragraphs(html: str) -> list[str]:
    m = _ARTICLE_RE.search(html)
    if not m:
        return []

    body = m.group("body")
    ps = []
    for pm in _P_RE.finditer(body):
        text = _TAG_RE.sub("", pm.group("p"))
        text = (
            text.replace("&apos;", "'")
            .replace("&quot;", '"')
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
        )
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            ps.append(text)
    return ps


_COOLDOWN_RE = re.compile(
    r"(?P<mins>\d+)\s*m(?:in(?:ute)?s?)?\s*(?P<secs>\d+)\s*s|(?P<secs_only>\d+)\s*s",
    re.IGNORECASE,
)


def _parse_cooldown_seconds(msg: str) -> Optional[int]:
    if "left to wait" not in msg.lower() and "wait" not in msg.lower():
        return None

    m = _COOLDOWN_RE.search(msg)
    if not m:
        return None

    if m.group("secs_only"):
        return int(m.group("secs_only"))

    mins = int(m.group("mins") or 0)
    secs = int(m.group("secs") or 0)
    return mins * 60 + secs


def _guess_high_low(msg: str) -> Optional[Literal["higher", "lower"]]:
    ml = msg.lower()
    if "too high" in ml:
        return "lower"
    if "too low" in ml:
        return "higher"
    return None


@dataclass(frozen=True)
class SubmitResult:
    ok: bool
    message: str
    direction: Optional[Literal["higher", "lower"]] = None
    cooldown_seconds: Optional[int] = None


def _submit(day: int, level: int, answer: str) -> SubmitResult:
    resp = _http().post(
        f"{AOC_BASE}/day/{day}/answer",
        data={"level": str(level), "answer": str(answer)},
        timeout=30,
    )
    resp.raise_for_status()

    paragraphs = _html_article_paragraphs(resp.text)
    msg = paragraphs[0] if paragraphs else resp.text

    ok = "right answer" in msg.lower()

    return SubmitResult(
        ok=ok,
        message=msg,
        direction=_guess_high_low(msg),
        cooldown_seconds=_parse_cooldown_seconds(msg),
    )


@lru_cache(maxsize=None)
def get_input(day: int) -> list[str]:
    r = _http().get(f"{AOC_BASE}/day/{day}/input", timeout=30)
    r.raise_for_status()
    return r.text.splitlines()


def submit_answer(
    *, day: int, level: Literal[1, 2] = 1, debug: bool = False
) -> Callable[[Callable[[], str]], Callable[[], str]]:
    def decorator(ans_fn: Callable[[], str]) -> Callable[[], str]:
        @wraps(ans_fn)
        def wrapped() -> str:
            answer = str(ans_fn())

            if debug:
                print(f"[debug] day {day} level {level} answer = {answer}")
                return answer

            try:
                result = _submit(day=day, level=level, answer=answer)
            except requests.RequestException as e:
                # Network / HTTP errors
                raise RuntimeError(
                    f"Failed to submit AoC answer (day={day}, level={level}): {e}"
                ) from e

            if result.ok:
                print("That's correct!")
            else:
                print(result.message)

                if result.direction:
                    print(f"Hint: try {result.direction}.")

                if result.cooldown_seconds is not None:
                    print(
                        f"Cooldown: {result.cooldown_seconds}s until you can try again."
                    )

            return answer

        return wrapped

    return decorator


def submit_answer1(*, day: int, debug: bool = False):
    return submit_answer(day=day, level=1, debug=debug)


def submit_answer2(*, day: int, debug: bool = False):
    return submit_answer(day=day, level=2, debug=debug)


def int_to_arr(n: int | str) -> list[int]:
    return [int(ch) for ch in str(n)]


def int_arr_to_int(n: list[int]) -> int:
    return int("".join(map(str, n)))
