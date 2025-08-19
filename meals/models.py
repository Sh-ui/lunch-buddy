from __future__ import annotations

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="meals")
    is_hearted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "category")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} ({self.category.name})"


class MealSnooze(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="snoozes")
    snooze_until = models.DateField()

    class Meta:
        ordering = ["-snooze_until"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Snooze {self.meal.name} until {self.snooze_until}"


