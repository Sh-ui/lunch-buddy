## Selection Algorithm

This document defines how Lunch Buddy composes weekly outputs from a tagged pantry (`var/pantry.json`). It replaces the earlier meal-only selector with a tag-driven composer capable of generating results like those in `docs/example-weeks.md`.

### Goals
- Produce three categories per day (Meal/Quick eat/Grab and go) that feel intentional, not random slop
- Enforce nutrition guardrails implicitly via ingredient roles/tags (high fiber, healthy fats; constrained carbs)
- Favor variety over weeks; respect user preferences (heart/snooze/archive)
- Keep rules simple, composable, and explainable

### Inputs
- Pantry items with attributes: type, tags, families, prep, methods, allowed_in, serve, forms, role, flavors, texture, constraints, is_pantry
- Weekly ingredient pool (8–10 items) chosen by generator or user
- History: past N weeks of generated recipes
- Preferences on items (hearted/snoozed/archived) — future extension at ingredient level

### Composition model (per category)
- Meal (Quick‑Cook)
  - Required: 1 main protein OR legume base; 1 leafy or firm veg; base (optional) from whole_grain; 1 flavor (sauce/dressing/dip)
  - Serve: hot is preferred; cold allowed if methods/serve support
  - Valid forms: bowl
- Quick eat (Prepped & Ready)
  - Required: base (wrap/pita/salad/bowl) + binder (dressing/dip/yogurt/tahini/peanut_butter) when needed + veg; protein optional if binder is protein‑rich
  - Serve: cold/room
  - Valid forms: salad, wrap, pita, bowl
- Grab and go
  - Required: snackable combo of 1–2 items (e.g., fruit + spread, veg + dip, cheese + crackers)
  - Serve: room/cold, no cook; forms: snack, toast, wrap

### Compatibility rules (hard constraints)
1. Use only items from the week pool plus pantry staples (`is_pantry: true`).
2. Obey `allowed_in` (category fit) and `serve` (e.g., romaine is cold only).
3. Respect `constraints`:
   - `no_heat` → not in Meal unless used cold; `no_microwave` → avoid microwave step; `messy_in_wrap` → avoid as the only binder in wraps; `needs_binder` (e.g., canned_tuna) → require a binder.
4. Family pairing: sauces prefer items sharing a cuisine family; neutral family is always allowed.

### Heuristics (soft scoring)
- Role balance per recipe
  - Meal target roles: main + filler + flavor (+ optional base). Penalize missing a flavor or veg.
  - Quick eat: base + binder + veg (+ optional main). Penalize if `needs_binder` is unmet.
  - Grab: topping|binder + base OR two snackables. Keep total 2–3 items.
- Nutrition nudges
  - Favor `high_fiber` veg and `whole_grain` bases; limit whole_grain appearances to ≤3 per week.
  - Favor `healthy_fat` sources across the week without doubling dip + creamy dressing in a single item.
- Variety
  - Avoid repeating the same main protein more than twice per week.
  - Rotate families (asian/mediterranean/latin/neutral) across days.

### Week assembly
1. Pick a week pool (if not user‑provided):
   - 2–3 proteins (mix of `lean_protein` and/or `legume`), 3–4 veg (leafy + firm + crunchy), 1–2 carbs (`whole_grain`), 2–3 flavors (sauce/dip/dressing).
2. Generate 6–9 recipes (2 per category or 1 per day depending on layout):
   - For each recipe slot, sample candidate sets that satisfy hard constraints, then score with heuristics and pick the highest.
3. Validate: no outside items; per‑week limits for carbs and repeats; every pool item appears ≥1 time.

### Pseudocode
```
for slot in week_slots:
  candidates = enumerate_combinations(pool, slot.category)
  candidates = filter_by_constraints(candidates, slot.category)
  for c in candidates:
    c.score = role_score(c) + nutrition_score(c, week_state) + variety_score(c, history)
  pick = argmax(candidates, key=score)
  commit(pick); update(week_state)
validate_week(week_state)
```

### Example mappings (from example-weeks)
- Shrimp + spinach + quinoa + soy_sauce → Meal: main=shrimp, filler=spinach, base=quinoa, flavor=soy (asian family, hot serve)
- Lentils + tomatoes + pesto in pita → Quick eat: base=pita, main=legume, flavor=pesto, serve=cold
- Peanut butter + banana on toast + honey → Grab: base=toast, binder=topping=peanut_butter, sweetener=honey

### History and preferences (carryover from meal selector)
- Maintain a per‑ingredient recency map; apply penalties to candidates that reuse the same main/family repeatedly across recent weeks.
- Hearts boost an item’s inclusion; snoozes/archives remove from consideration.

### Outputs
- Printable week with grocery section (pool) and categorized recipes consistent with `docs/example-weeks.md`.

