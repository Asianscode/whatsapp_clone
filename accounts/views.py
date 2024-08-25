# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from accounts.forms import OTPForm
from django.contrib.auth.models import User
from .models import OTP
import random
import string
import logging
from datetime import datetime, timedelta

# Get an instance of a logger
logger = logging.getLogger(__name__)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp_code):
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp_code}',
        'me2020boy@gmail.com',  # replace with your email
        [email],
        fail_silently=False,
    )

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        user, created = User.objects.get_or_create(username=email, email=email)
        
        if created:
            otp_code = random.randint(100000, 999999)
            OTP.objects.create(user=user, code=otp_code)

            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp_code}',
                'your_email@example.com',
                [email],
                fail_silently=False,
            )
            return redirect('otp_verify', user_id=user.id)
    return render(request, 'accounts/register.html')

def otp_verify(request, user_id):
    if request.method == 'POST':
        otp_code = request.POST['otp']
        try:
            otp = OTP.objects.get(user_id=user_id, code=otp_code)
            if otp.is_valid():
                return redirect('account_creation', user_id=user_id)
            else:
                return render(request, 'accounts/otp_verify.html', {'error': 'Invalid or expired OTP.'})
        except OTP.DoesNotExist:
            return render(request, 'accounts/otp_verify.html', {'error': 'Invalid OTP.'})
    return render(request, 'accounts/otp_verify.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the home page or another page after login
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login_view')

def account_creation(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        username = request.POST['username']
        phone_number = request.POST['phone_number']
        profile_picture = request.FILES['profile_picture']

        user.username = username
        user.profile.phone_number = phone_number
        user.profile.profile_picture = profile_picture
        user.save()

        return redirect('home')
    return render(request, 'accounts/account_creation.html', {'user': user})
