from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def front_page(request: HttpRequest):
    return render(request, 'game/index.html')
