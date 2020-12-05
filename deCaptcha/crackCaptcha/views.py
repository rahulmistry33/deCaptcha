from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request,'crackCaptcha/index.html')


def crack(request):
    return render(request,'crackCaptcha/crack.html')