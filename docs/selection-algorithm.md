## Selection Algorithm

### Goals
- Favor variety by penalizing recent repeats
- Respect user intent: snoozes exclude; hearts boost
- Stay simple and predictable; configurable weights

### Inputs
- Available meals per category (exclude archived and snoozed)
- Recent history window W (e.g., 3–4 weeks)
- Heart boost multiplier H (e.g., 1.15)
- Recency penalties P = [p1, p2, p3, ...] per week back (e.g., [0.0, 0.3, 0.6])

### Weighting
For each candidate meal m:
- Start with base weight 1.0
- If m appears in week t back (t = 1..W): weight = min(weight, P[t])
  - Example defaults: week1 → 0.0 (hard exclude), week2 → 0.3, week3 → 0.6; older → 1.0
- If `is_hearted`: weight = weight * H
- Clamp to [0.0, 1.0]

### Selection Process
- For each day/category slot, compute weights over remaining candidates
- Remove meals selected earlier in the same week to avoid duplicates
- Use `random.choices` with weights; if all weights 0 for a category, relax by ignoring week3 penalty first, then week2, etc.
- Optional: deterministic seed based on `week_start` for reproducible generation

### Config Defaults (MVP)
- W = 3 weeks
- P = [0.0, 0.3, 0.6]
- H = 1.15

### Edge Cases
- Small pools: allow controlled relaxation to avoid dead-ends
- Conflicts: limit re-roll attempts; surface a warning to the user
- Snoozes expiring mid-week: resolved at generation time only

### Validation
- Assert no duplicate meals in the plan
- Assert no hard-excluded meals selected
