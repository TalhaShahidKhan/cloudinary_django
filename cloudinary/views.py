from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request,"cloud/home.html")


def ai_task(request):
    return render(request,"cloud/ai.html")