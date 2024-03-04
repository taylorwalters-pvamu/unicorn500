from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def demo(request):
    return render(request, 'demo.html')

def support(request):
    return render(request, 'support.html')

def adapter(request):
    return render(request, 'adapter.html')

def u_auth(request):
    return render(request, 'user_authent.html')