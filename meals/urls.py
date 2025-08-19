from django.urls import path
from . import views


urlpatterns = [
    path('', views.meal_list, name='meal_list'),
    path('add/', views.meal_create, name='meal_create'),
    path('<int:pk>/edit/', views.meal_update, name='meal_update'),
    path('<int:pk>/toggle-heart/', views.toggle_heart, name='toggle_heart'),
    path('<int:pk>/toggle-archive/', views.toggle_archive, name='toggle_archive'),
    path('<int:pk>/snooze/', views.snooze_meal, name='snooze_meal'),
]


