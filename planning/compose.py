from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Iterable


def _has(item: dict, key: str, value: str) -> bool:
    return value in (item.get(key) or [])


def _tag(item: dict, value: str) -> bool:
    return value in (item.get("tags") or [])


def load_pantry(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _pick(items: Iterable[dict], predicate) -> dict | None:
    candidates = [i for i in items if predicate(i)]
    return random.choice(candidates) if candidates else None


def _family_match(a: dict | None, b: dict | None) -> bool:
    if not a or not b:
        return True
    fa = set(a.get("families") or [])
    fb = set(b.get("families") or [])
    return bool((fa & fb) or "neutral" in fa or "neutral" in fb)


def generate_sample_week(pantry: dict, seed: int | None = None) -> dict[str, list[str]]:
    if seed is not None:
        random.seed(seed)

    items: list[dict[str, Any]] = pantry.get("ingredients", [])
    non_pantry = [i for i in items if not i.get("is_pantry")]

    # Convenience typed subsets
    proteins = [i for i in non_pantry if i.get("type") == "protein" or _tag(i, "legume")]
    vegs_hot = [i for i in non_pantry if i.get("type") in {"vegetable", "fruit"} and ("hot" in (i.get("serve") or []) or "saute_green" in (i.get("tags") or []))]
    vegs_cold = [i for i in non_pantry if i.get("type") in {"vegetable", "fruit"} and "cold" in (i.get("serve") or [])]
    bases_hot = [i for i in non_pantry if _tag(i, "whole_grain") and "hot" in (i.get("serve") or []) and i.get("type") == "carb"]
    bases_wrap = [i for i in non_pantry if "wrap" in (i.get("forms") or []) or "pita" in (i.get("forms") or []) or "toast" in (i.get("forms") or [])]
    sauces = [i for i in non_pantry if i.get("type") in {"sauce", "dressing", "dip"}]

    meals: list[str] = []
    quicks: list[str] = []
    grabs: list[str] = []

    # Meal 1: hot bowl
    p1 = _pick(proteins, lambda i: "hot" in (i.get("serve") or []) or i.get("type") == "protein")
    v1 = _pick(vegs_hot, lambda i: True)
    b1 = _pick(bases_hot, lambda i: True)
    s1 = _pick(sauces, lambda s: _family_match(s, p1))
    if p1 and v1 and b1 and s1:
        meals.append(f"{p1['name']} + {v1['name']} + {b1['name']} + {s1['name']}")

    # Meal 2: simple soup if lentils present
    lentils = _pick(items, lambda i: i.get("key") == "lentils")
    carrots = _pick(items, lambda i: i.get("key") == "carrots")
    pita = _pick(items, lambda i: i.get("key") == "pita_bread_whole_wheat")
    pesto = _pick(items, lambda i: i.get("key") == "pesto")
    if lentils and carrots:
        suffix = f"; serve with {pita['name']} and {pesto['name']}" if pita and pesto else ""
        meals.append(f"Simple lentil–carrot soup{suffix}")

    # Quick eat 1: wrap/pita with binder (handles tuna needs_binder)
    base_wrap = _pick(bases_wrap, lambda i: True)
    veg_c = _pick(vegs_cold, lambda i: True)
    binder = _pick(sauces, lambda s: s.get("type") in {"dressing", "dip", "sauce"} or "binder" in (s.get("role") or []))
    p2 = _pick(proteins, lambda i: True)
    if base_wrap and veg_c and binder:
        if p2 and _has(p2, "constraints", "needs_binder") and not binder:
            p2 = None  # fallback to veg+binder
        parts = [p for p in [p2 and p2["name"], veg_c["name"], base_wrap["name"], binder["name"]] if p]
        quicks.append(" + ".join(parts))

    # Quick eat 2: cold bowl
    qb = _pick(items, lambda i: _has(i, "forms", "bowl") and "cold" in (i.get("serve") or []) and (i.get("type") in {"carb", "protein"} or _tag(i, "legume")))
    vq = _pick(vegs_cold, lambda i: True)
    sq = _pick(sauces, lambda s: True)
    if qb and vq and sq:
        quicks.append(f"{qb['name']} bowl with {vq['name']} + {sq['name']}")

    # Grab-and-go 1: pb banana toast if available
    pb = _pick(items, lambda i: i.get("key") == "peanut_butter")
    banana = _pick(items, lambda i: i.get("key") == "bananas")
    bread = _pick(items, lambda i: i.get("key") == "whole_grain_bread")
    honey = _pick(items, lambda i: i.get("key") == "honey")
    if pb and banana and bread:
        grabs.append(f"{pb['name']} + {banana['name']} on {bread['name']}" + (f" + {honey['name']}" if honey else ""))

    # Grab-and-go 2: veg + dip or cheese + crackers
    dip = _pick(sauces, lambda s: s.get("type") == "dip")
    crunchy = _pick(items, lambda i: "crunchy_veg" in (i.get("tags") or []))
    cheese = _pick(items, lambda i: i.get("key") == "cheese_cubes")
    crackers = _pick(items, lambda i: i.get("key") == "whole_wheat_crackers")
    if crunchy and dip:
        grabs.append(f"{crunchy['name']} + {dip['name']}")
    elif cheese and crackers:
        grabs.append(f"{cheese['name']} + {crackers['name']}")

    return {"meal": meals, "quick_eat": quicks, "grab_and_go": grabs}


