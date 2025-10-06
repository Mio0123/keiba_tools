from django.contrib import admin
from django.urls import path
from race import views as race_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', race_views.health_check, name='health_check'),

    # ▼▼▼ 以下2行を新しく追加 ▼▼▼
    path('reception/', race_views.race_list, name='race_list'),
    path('reception/race/<int:race_id>/', race_views.betting_form, name='betting_form'),
]