from django.shortcuts import render


# Create your views here.
def main(request):
    return render(request, "mainUI/index.html")
def editor(request):
    return render(request, "mainUI/index.html")

def homepage(request):
    return render(request, "mainUI/homepage.html")


def sidebar(request):
    return render(request, "mainUI/sidebar.html")


def testing(request):
    return render(request, "mainUI/testing.html")



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
import json

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.name}!')
                
                # Redirect to next parameter if exists
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    else:
        form = UserLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
        'file_store': user.file_store,
        'main_file': user.main_file,
    }
    return render(request, 'authentication/dashboard.html', context)

@login_required
def update_file_store_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            file_store_data = data.get('file_store', {})
            
            # Update the user's file_store
            request.user.file_store = file_store_data
            request.user.save()
            
            return JsonResponse({'status': 'success', 'message': 'FileStore updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def update_main_file_view(request):
    if request.method == 'POST':
        main_file = request.POST.get('main_file')
        if main_file:
            request.user.main_file = main_file
            request.user.save()
            messages.success(request, 'Main file updated successfully')
        else:
            messages.error(request, 'Main file name is required')
        return redirect('dashboard')
    
    return redirect('dashboard')

@login_required
def get_user_profile_view(request):
    user = request.user
    profile_data = {
        'email': user.email,
        'name': user.name,
        'main_file': user.main_file,
        'file_store': user.file_store,
        'date_joined': user.date_joined.isoformat(),
    }
    return JsonResponse(profile_data)
