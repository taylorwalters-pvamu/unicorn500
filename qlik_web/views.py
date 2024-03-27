from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def demo(request):
    return render(request, 'demo.html')

def support(request):
    return render(request, 'support.html')

def adapter(request):
    return render(request, 'adapter.html')
