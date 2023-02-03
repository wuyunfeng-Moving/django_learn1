from django.http import HttpResponse
from django.shortcuts import render

test_num = 20


def home(request):
    return render(request, "templates/home.html")

