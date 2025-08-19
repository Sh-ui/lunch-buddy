from __future__ import annotations

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Meal, Category
from .forms import MealForm, MealSnoozeForm


def meal_list(request):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')
    meals = Meal.objects.select_related('category').order_by('name')
    categories = Category.objects.order_by('name')
    if q:
        meals = meals.filter(name__icontains=q)
    if category_id:
        meals = meals.filter(category_id=category_id)
    return render(request, 'meals/list.html', {
        'meals': meals,
        'categories': categories,
        'q': q,
        'category_id': category_id,
    })


@require_http_methods(["GET", "POST"])
def meal_create(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meal_list')
    else:
        form = MealForm()
    return render(request, 'meals/form.html', {'form': form, 'title': 'Add Meal'})


@require_http_methods(["GET", "POST"])
def meal_update(request, pk: int):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('meal_list')
    else:
        form = MealForm(instance=meal)
    return render(request, 'meals/form.html', {'form': form, 'title': 'Edit Meal'})


@require_http_methods(["POST"]) 
def toggle_heart(request, pk: int):
    meal = get_object_or_404(Meal, pk=pk)
    meal.is_hearted = not meal.is_hearted
    meal.save(update_fields=['is_hearted'])
    return redirect(request.META.get('HTTP_REFERER', reverse('meal_list')))


@require_http_methods(["POST"]) 
def toggle_archive(request, pk: int):
    meal = get_object_or_404(Meal, pk=pk)
    meal.is_archived = not meal.is_archived
    meal.save(update_fields=['is_archived'])
    return redirect(request.META.get('HTTP_REFERER', reverse('meal_list')))


@require_http_methods(["GET", "POST"]) 
def snooze_meal(request, pk: int):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == 'POST':
        form = MealSnoozeForm(request.POST)
        if form.is_valid():
            snooze = form.save(commit=False)
            snooze.meal = meal
            snooze.save()
            return redirect('meal_list')
    else:
        form = MealSnoozeForm()
    return render(request, 'meals/snooze.html', {'form': form, 'meal': meal})


