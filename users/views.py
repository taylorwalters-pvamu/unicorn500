from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def login_user(request):
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
            return render(request, 'login.html')  # Redirect to adapter page on successful login
    else:
        return render(request, 'authenticate/login.html')