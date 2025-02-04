from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import StudentRegistrationForm, LoginForm
import random
import string

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            password = generate_password()
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=password
            )
            
            student = form.save(commit=False)
            student.user = user
            student.save()
            
            subject = 'Your Student ID Card System Password'
            message = f"Hi {user.username},\n\nYour password is: {password}\n\nPlease login using these credentials."
            user.email_user(subject, message)
            
            messages.success(request, 'Registration successful! Please check your email for login credentials.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('id_card')
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def id_card(request):
    student = request.user.student
    return render(request, 'id_card.html', {'student': student})

def user_logout(request):
    logout(request)
    return redirect('register')

