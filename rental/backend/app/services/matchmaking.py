from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.models.enums import SleepCycle


@dataclass(frozen=True)
class LifestyleInput:
    is_smoker: bool
    sleep_cycle: SleepCycle | str
    job_type: str | None


def _normalize_sleep_cycle(value: SleepCycle | str | Any) -> str:
    if isinstance(value, SleepCycle):
        return value.value
    return str(value or "").strip().lower()


def _normalize_job_type(value: str | None | Any) -> str:
    return str(value or "").strip().lower()


def _sleep_alignment_score(user_sleep: str, listing_sleep: str) -> float:
    if not user_sleep or not listing_sleep:
        return 0.0
    if user_sleep == listing_sleep:
        return 30.0
    if {
        user_sleep,
        listing_sleep,
    } == {
        SleepCycle.NORMAL.value,
        SleepCycle.NIGHT_OWL.value,
    } or {
        user_sleep,
        listing_sleep,
    } == {
        SleepCycle.NORMAL.value,
        SleepCycle.EARLY_BIRD.value,
    }:
        return 12.0
    return 0.0


def calculate_match_score(user_prefs: dict, listing_prefs: dict) -> float:
    """
    Weighted compatibility score (0-100) with a 20-point floor.

    Weights:
    - smoking habits: 50
    - sleep cycle alignment: 30
    - job type similarity: 20
    """
    score = 0.0
    min_floor = 20.0

    user_smoker = bool(user_prefs.get("is_smoker", False))
    listing_smoker = bool(listing_prefs.get("is_smoker", False))
    if user_smoker == listing_smoker:
        score += 50.0

    user_sleep = _normalize_sleep_cycle(user_prefs.get("sleep_cycle"))
    listing_sleep = _normalize_sleep_cycle(listing_prefs.get("sleep_cycle"))
    score += _sleep_alignment_score(user_sleep, listing_sleep)

    user_job = _normalize_job_type(user_prefs.get("job_type"))
    listing_job = _normalize_job_type(listing_prefs.get("job_type"))
    if user_job and listing_job and user_job == listing_job:
        score += 20.0

    return round(max(min_floor, score), 2)


def calculate_match_percentage(
    user_lifestyle: LifestyleInput | Any,
    mess_lifestyle: LifestyleInput | Any,
) -> float:
    """
    Calculate lifestyle match percentage (0-100) for Bachelor matchmaking.

    Rules:
    - Both same smoker preference => +40%
    - Same sleep cycle => +30%
    - Same job type => +30%
    """
    user_prefs = {
        "is_smoker": getattr(user_lifestyle, "is_smoker", False),
        "sleep_cycle": getattr(user_lifestyle, "sleep_cycle", ""),
        "job_type": getattr(user_lifestyle, "job_type", None),
    }
    listing_prefs = {
        "is_smoker": getattr(mess_lifestyle, "is_smoker", False),
        "sleep_cycle": getattr(mess_lifestyle, "sleep_cycle", ""),
        "job_type": getattr(mess_lifestyle, "job_type", None),
    }
    return calculate_match_score(user_prefs, listing_prefs)

