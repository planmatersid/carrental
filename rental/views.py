from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Car, UserProfile
from .forms import CarForm, SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'rental/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        login_option = request.POST.get('login_option') 
        username = request.POST['username']
        password = request.POST['password']
        if login_option == 'login_as_user':
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('user_home')
            else:
                messages.error(request, 'Invalid credentials')
        elif login_option == 'login_as_admin':
            user = authenticate(request, username=username, password=password)
            if user and user.is_superuser:
                login(request, user)
                return redirect('admin_home')
            else:
                messages.error(request, 'Invalid admin credentials')
    return render(request, 'rental/login.html')


@login_required
def admin_home(request):
    if not request.user.is_superuser:
        return redirect('login')
    cars = Car.objects.all()
    return render(request, 'rental/admin_home.html', {'cars': cars})


@login_required
def add_car(request):
    if not request.user.is_superuser:
        return redirect('login')
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = CarForm()
    return render(request, 'rental/add_car.html', {'form': form})


@login_required
def user_home(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'rental/user_home.html', {'cars': cars})


def rent_car(request, car_id):
    car = Car.objects.get(id=car_id)
    return redirect('payment') 
from django.contrib import messages


def payment_page(request):
    if request.method == 'POST':
        name = request.POST['Name']
        address = request.POST['Address']
        time = request.POST['Time']
        messages.success(request, f'Thank you, {name}, for renting with us! Kindly return the car after {time} days')
        return redirect('user_home')
    return render(request, 'rental/payment.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def remove_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    return redirect('admin_home') 