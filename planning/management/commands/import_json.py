from __future__ import annotations

import json
import sys
from django.core.management.base import BaseCommand, CommandError
from meals.models import Category, Meal


class Command(BaseCommand):
    help = "Import categories and meals from JSON stdin or file path"

    def add_arguments(self, parser):
        parser.add_argument("path", nargs="?", help="Path to JSON file; defaults to stdin")

    def handle(self, *args, **options):
        data: dict
        try:
            if options.get("path"):
                with open(options["path"], "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = json.load(sys.stdin)
        except Exception as exc:  # pragma: no cover
            raise CommandError(f"Failed to read JSON: {exc}")

        name_to_cat: dict[str, Category] = {}
        for cat in data.get("categories", []):
            obj, _ = Category.objects.get_or_create(name=cat["name"]) 
            name_to_cat[obj.name] = obj

        for m in data.get("meals", []):
            category = name_to_cat.get(m["category"]) or Category.objects.get_or_create(name=m["category"])[0]
            Meal.objects.get_or_create(
                name=m["name"],
                category=category,
                defaults={
                    "is_hearted": bool(m.get("hearted", False)),
                    "is_archived": bool(m.get("archived", False)),
                },
            )
        self.stdout.write(self.style.SUCCESS("Import complete"))


