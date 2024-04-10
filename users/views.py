from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib import messages
from .form import RegisterUserForm
# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
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
    
def logout_user(request):
    logout(request)
    messages.success(request, 'Active session ended. Login to continue.')
    return redirect('login')

user = get_user_model()
def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.username = var.email
            var.is_customer = True
            var.save()
            messages.success(request, "Account created. Please log in.")
            return redirect('login')
        else:
            messages.warning(request, 'Something went wrong. Please check for errors.')
            return redirect('register_customer')
    else:
        form = RegisterUserForm()
        context = {'fomr': form}
        return render(request, 'user/register_customer.html', context)
