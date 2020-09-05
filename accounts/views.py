from django.shortcuts import render, redirect
from .forms import Register,Login
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# Create your views here.


def register(request):
    if request.method == "POST":
        user_form = Register(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = Register()
    return render(request, 'register.html', {'user_form': user_form})
    
def login(request):
    if request.method == 'POST':
        log_form =Login(data=request.POST)
        if log_form.is_valid():
            return redirect('main')
    else:
        log_form = Login()
    return render(request, 'login.html', {'log_form': log_form})


def logout(request):
    login.logout(request)
    return redirect('main')
