from django.contrib import admin
from django.urls import path
from django.http import HttpResponse  # ← HttpResponseを直接インポートします

# --- デバッグ用のビュー関数を、このファイルに直接定義します ---
def health_check_direct(request):
    return HttpResponse("Health check OK from urls.py itself.")
# ---------------------------------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    # 'race'アプリのビューを使わず、上で定義した関数を直接指定します
    path('health/', health_check_direct, name='health_check'),
]