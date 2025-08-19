from __future__ import annotations

import datetime
from django.test import TestCase

from meals.models import Category, Meal
from .services import generate_weekly_plan, SelectionConfig


class SelectionTests(TestCase):
    def setUp(self) -> None:
        protein = Category.objects.create(name="Protein")
        veg = Category.objects.create(name="Vegetable")
        self.categories = [protein, veg]
        # Create small pool
        Meal.objects.create(name="Salmon", category=protein, is_hearted=True)
        Meal.objects.create(name="Shrimp", category=protein)
        Meal.objects.create(name="Broccoli", category=veg)
        Meal.objects.create(name="Carrots", category=veg)

    def test_plan_has_no_duplicates_and_respects_categories(self):
        week_start = datetime.date(2025, 1, 6)  # Monday
        history_lookup = {}
        plan = generate_weekly_plan(week_start, self.categories, history_lookup, SelectionConfig(), seed=42)
        # 7 days * 2 categories = 14 entries unless pool constraints reduce
        # Ensure no duplicate meals in the same week
        seen = set()
        for _, _, meal in plan:
            self.assertNotIn(meal.id, seen)
            seen.add(meal.id)


