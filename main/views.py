from django.shortcuts import render,redirect
from .models import Expenses
from .forms import MyExpenses, Register, UserLoginForm
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required



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


def user_login(request):
    if request.method == 'POST':
        log_form = UserLoginForm(request.POST)
        if log_form.is_valid():
            username = log_form.cleaned_data['username']
            password = log_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                contex = {
                    'log_form':UserLoginForm(),
                    'error': 'Username or Password Incorrect'
                    
                }
                return render(request,'login.html',contex)
        print("Login Successfully")
    else:
        log_form =UserLoginForm()
    return render(request, 'login.html', {'log_form': log_form})


def logout(request):
    django_logout(request)
    return redirect('/')


def main(request):
    return render(request, 'main.html')

@login_required(login_url='login')
def data(request):
    exps = Expenses.objects.all()
    return render(request, 'data.html', {'exps':exps})


@login_required(login_url='login')
def form(request):
    if request.method == 'POST':
        exp_form = MyExpenses(request.POST)
        if exp_form.is_valid():
            exp_form.save()
        return redirect('main')

    else:
        exp_form = MyExpenses()
    return render(request, 'form.html', {'exp_form': exp_form})


    

