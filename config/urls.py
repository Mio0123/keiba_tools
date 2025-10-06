from django.contrib import admin
from django.urls import path
from race import views as race_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', race_views.health_check, name='health_check'),
]