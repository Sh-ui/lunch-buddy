from __future__ import annotations

from django.db import models
from meals.models import Category, Meal


class WeeklyPlan(models.Model):
    week_start = models.DateField(help_text="ISO Monday of the week")
    pdf_path = models.CharField(max_length=512, blank=True)
    liked = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-week_start"]
        unique_together = ("week_start",)

    def __str__(self) -> str:  # pragma: no cover
        return f"Week of {self.week_start}"


class PlanEntry(models.Model):
    DAY_CHOICES = [
        ("Mon", "Mon"), ("Tue", "Tue"), ("Wed", "Wed"),
        ("Thu", "Thu"), ("Fri", "Fri"), ("Sat", "Sat"), ("Sun", "Sun"),
    ]

    plan = models.ForeignKey(WeeklyPlan, on_delete=models.CASCADE, related_name="entries")
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("plan", "day", "category")
        ordering = ["plan_id", "day", "category_id"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.day}: {self.category.name} → {self.meal.name}"


