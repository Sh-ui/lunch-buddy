from django.urls import path
from . import views


urlpatterns = [
    path('generate/', views.generate_upcoming, name='generate_upcoming'),
    path('week/<slug:week_start>/', views.plan_detail, name='plan_detail'),
    path('week/<slug:week_start>/regenerate/', views.plan_regenerate, name='plan_regenerate'),
    path('week/<slug:week_start>/like/', views.plan_like, name='plan_like'),
    path('week/<slug:week_start>/dislike/', views.plan_dislike, name='plan_dislike'),
    path('history/', views.history_list, name='history_list'),
]


