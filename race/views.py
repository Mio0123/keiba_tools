from django.shortcuts import render
from django.http import HttpResponse

# このファイルには、データベースを使わないシンプルなビューのみを定義します
def health_check(request):
    return HttpResponse("Hello, Vercel! Health check from race.views is OK.")