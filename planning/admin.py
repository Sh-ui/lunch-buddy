from django.contrib import admin
from .models import WeeklyPlan, PlanEntry


class PlanEntryInline(admin.TabularInline):
    model = PlanEntry
    extra = 0


@admin.register(WeeklyPlan)
class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = ("week_start", "liked", "created_at")
    list_filter = ("liked",)
    inlines = [PlanEntryInline]


