## Data Model

### Entities
- **Category**
  - id, name (e.g., Protein, Vegetable, Carb)
- **Meal**
  - id, name, category_id, is_hearted (bool), is_archived (bool)
- **MealSnooze**
  - id, meal_id, snooze_until (date)
- **WeeklyPlan**
  - id, week_start (date ISO Monday), pdf_path, liked (nullable bool), created_at
- **PlanEntry**
  - id, plan_id, day (Mon..Sun), category_id, meal_id

### Constraints
- Meal cannot be selected if snoozed (today < snooze_until)
- No duplicate meal in the same `WeeklyPlan`
- Avoid meals used in the previous N weeks per weighting policy

### JSON Import/Export (for backup)
```
{
  "categories": [
    {"name": "Protein"}, {"name": "Vegetable"}, {"name": "Carb"}
  ],
  "meals": [
    {"name": "Salmon", "category": "Protein", "hearted": true, "archived": false},
    {"name": "Shrimp", "category": "Protein", "hearted": false, "archived": false}
  ],
  "history": [
    {
      "week_start": "2025-02-17",
      "liked": true,
      "entries": [
        {"day": "Mon", "category": "Protein", "meal": "Salmon"}
      ]
    }
  ]
}
```

### Admin UX
- Inline editing of meals
- Filters: category, hearted, snoozed active, archived
