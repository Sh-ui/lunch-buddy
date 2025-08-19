from django.contrib import admin
from .models import Category, Meal, MealSnooze


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_hearted", "is_archived")
    list_filter = ("category", "is_hearted", "is_archived")
    search_fields = ("name",)


@admin.register(MealSnooze)
class MealSnoozeAdmin(admin.ModelAdmin):
    list_display = ("meal", "snooze_until")
    list_filter = ("snooze_until",)
    autocomplete_fields = ("meal",)


