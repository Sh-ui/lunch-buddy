from django.contrib import admin
from django.urls import path, include
from web.views import home, pantry


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('pantry/', pantry, name='pantry'),
    path('meals/', include('meals.urls')),
    path('planning/', include('planning.urls')),
]


