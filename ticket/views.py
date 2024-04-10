from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import SupportTicketForm

# Create your views here.
def submit_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            subject = 'New Support Ticket'
            message = f"Subject: {form.cleaned_data['title']}\n\nDescription: {form.cleaned_data['description']}"
            recipient_list = [admin_email for name, admin_email in settings.ADMINS]  # Assuming you have specified ADMINS in settings.py
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            return redirect('support')  # Redirect to a success page
    else:
        form = SupportTicketForm()
    return render(request, 'support.html', {'form': form})