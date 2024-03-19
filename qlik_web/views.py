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

def u_auth(request):
    return render(request, 'user_authent.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Debugging: Print a message to verify successful authentication
            print("User authenticated successfully")
            return redirect('adapter')  # Redirect to adapter page on successful login
        else:
            error_message = "Invalid username or password"
            messages.error(request, error_message)
            return render(request, 'adapter.html')  # Redirect to adapter page on successful login
    else:
        return render(request, 'login.html')