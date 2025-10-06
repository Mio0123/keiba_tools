from django.contrib import admin
from django.urls import path
from race import views as race_views  # ← この行を追加

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', race_views.health_check, name='health_check'),  # ← この行を追加
]