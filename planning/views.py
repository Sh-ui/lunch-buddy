from __future__ import annotations

import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from meals.models import Category
from .models import WeeklyPlan, PlanEntry
from .services import generate_weekly_plan, SelectionConfig


def _get_categories() -> list[Category]:
    return list(Category.objects.order_by('name'))


def _week_monday(date: datetime.date) -> datetime.date:
    return date - datetime.timedelta(days=date.weekday())


def history_list(request):
    plans = WeeklyPlan.objects.order_by('-week_start').all()
    return render(request, 'planning/history.html', {'plans': plans})


def plan_detail(request, week_start: str):
    week = datetime.date.fromisoformat(week_start)
    plan = get_object_or_404(WeeklyPlan, week_start=week)
    entries = plan.entries.select_related('meal', 'category').all()
    return render(request, 'planning/detail.html', {'plan': plan, 'entries': entries})


def generate_upcoming(request):
    today = datetime.date.today()
    next_monday = _week_monday(today + datetime.timedelta(days=7))
    return _generate_for_week(next_monday)


def plan_regenerate(request, week_start: str):
    week = datetime.date.fromisoformat(week_start)
    return _generate_for_week(week, overwrite=True)


def _generate_for_week(week_start: datetime.date, overwrite: bool = False):
    # Collect history sets for penalties
    history_lookup: dict[int, set[int]] = {}
    categories = _get_categories()
    # last W weeks meal ids
    W = SelectionConfig().recent_weeks
    for t in range(1, W + 1):
        week = week_start - datetime.timedelta(days=7 * t)
        ids = set(
            PlanEntry.objects.filter(plan__week_start=week).values_list('meal_id', flat=True)
        )
        if ids:
            history_lookup[t] = ids

    seed = int(week_start.strftime('%Y%m%d'))
    rows = generate_weekly_plan(week_start, categories, history_lookup, SelectionConfig(), seed=seed)

    plan, _ = WeeklyPlan.objects.get_or_create(week_start=week_start)
    if overwrite:
        plan.entries.all().delete()
    obj_list = [
        PlanEntry(plan=plan, day=day, category=cat, meal=meal)
        for day, cat, meal in rows
    ]
    PlanEntry.objects.bulk_create(obj_list)
    return redirect('plan_detail', week_start=week_start.isoformat())


@require_http_methods(["POST"]) 
def plan_like(request, week_start: str):
    week = datetime.date.fromisoformat(week_start)
    plan = get_object_or_404(WeeklyPlan, week_start=week)
    plan.liked = True
    plan.save(update_fields=['liked'])
    return redirect('plan_detail', week_start=week_start)


@require_http_methods(["POST"]) 
def plan_dislike(request, week_start: str):
    week = datetime.date.fromisoformat(week_start)
    plan = get_object_or_404(WeeklyPlan, week_start=week)
    plan.liked = False
    plan.save(update_fields=['liked'])
    return redirect('plan_detail', week_start=week_start)


