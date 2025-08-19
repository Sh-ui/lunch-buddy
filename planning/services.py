from __future__ import annotations

import datetime
import random
from dataclasses import dataclass
from typing import Iterable, Sequence

from meals.models import Meal, Category


@dataclass
class SelectionConfig:
    recent_weeks: int = 3  # W
    penalties: Sequence[float] = (0.0, 0.3, 0.6)  # P
    heart_boost: float = 1.15  # H


def compute_available_meals(today: datetime.date) -> Iterable[Meal]:
    # Exclude archived and active snoozes
    qs = Meal.objects.filter(is_archived=False).exclude(
        snoozes__snooze_until__gt=today
    )
    return qs.select_related("category").distinct()


def weighted_choice(meals: Sequence[Meal], weights: Sequence[float]) -> Meal:
    return random.choices(meals, weights=weights, k=1)[0]


def generate_weekly_plan(
    week_start: datetime.date,
    categories: Sequence[Category],
    history_lookup: dict[int, set[int]],
    config: SelectionConfig,
    seed: int | None = None,
) -> list[tuple[str, Category, Meal]]:
    if seed is not None:
        random.seed(seed)

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    today = week_start
    available = list(compute_available_meals(today))
    plan: list[tuple[str, Category, Meal]] = []
    selected_meal_ids: set[int] = set()

    for day in days:
        for category in categories:
            # Candidates of this category not already picked this week
            candidates = [m for m in available if m.category_id == category.id and m.id not in selected_meal_ids]
            if not candidates:
                continue
            # Base weights
            weights: list[float] = [1.0 for _ in candidates]
            # Apply recency penalties
            for idx, meal in enumerate(candidates):
                w = 1.0
                for t in range(1, config.recent_weeks + 1):
                    if meal.id in history_lookup.get(t, set()):
                        w = min(w, config.penalties[t - 1])
                if meal.is_hearted:
                    w *= config.heart_boost
                weights[idx] = max(0.0, min(1.0, w))

            # Relaxation if all zero
            relax = config.recent_weeks - 1
            while sum(weights) == 0.0 and relax >= 0:
                for idx, meal in enumerate(candidates):
                    w = 1.0
                    for t in range(1, relax + 1):
                        if meal.id in history_lookup.get(t, set()):
                            w = min(w, config.penalties[t - 1])
                    if meal.is_hearted:
                        w *= config.heart_boost
                    weights[idx] = max(0.0, min(1.0, w))
                relax -= 1

            chosen = weighted_choice(candidates, weights)
            plan.append((day, category, chosen))
            selected_meal_ids.add(chosen.id)

    # Basic validations
    assert len({(d, c.id) for d, c, _ in plan}) == len(plan)
    assert not any(m.id in history_lookup.get(1, set()) for _, _, m in plan)
    return plan


