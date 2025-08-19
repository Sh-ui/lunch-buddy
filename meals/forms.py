from __future__ import annotations

from django import forms
from .models import Meal, MealSnooze


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["name", "category", "is_hearted", "is_archived"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Salmon"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "is_hearted": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_archived": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class MealSnoozeForm(forms.ModelForm):
    class Meta:
        model = MealSnooze
        fields = ["snooze_until"]
        widgets = {
            "snooze_until": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


