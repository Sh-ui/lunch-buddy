from __future__ import annotations

import json
from django.core.management.base import BaseCommand
from meals.models import Category, Meal


class Command(BaseCommand):
    help = "Export basic data to JSON"

    def handle(self, *args, **options):
        categories = list(Category.objects.all().values("name"))
        meals = [
            {
                "name": m.name,
                "category": m.category.name,
                "hearted": m.is_hearted,
                "archived": m.is_archived,
            }
            for m in Meal.objects.select_related("category")
        ]
        payload = {"categories": categories, "meals": meals}
        self.stdout.write(json.dumps(payload, indent=2))


