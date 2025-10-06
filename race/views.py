from django.shortcuts import render

# Create your views here.
# race/views.py
from django.http import HttpResponse

# ... ファイルの末尾に追加 ...
def health_check(request):
    return HttpResponse("Hello, Vercel! Django is running correctly.")