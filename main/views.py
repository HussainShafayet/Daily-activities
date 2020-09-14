from django.shortcuts import render,redirect
from .models import Expenses,Category
from .forms import MyExpenses, Register, UserLoginForm,Add_category
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
    return redirect('main')


def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def data(request, id):
    current_user=request.user
    exps = Expenses.objects.filter(user=current_user,category__id=id)
    return render(request, 'data.html', {'exps':exps})


@login_required(login_url='login')
def form(request):
    if request.method == 'POST':
        exp_form = MyExpenses(request.user,request.POST)
        if exp_form.is_valid():
            exp = Expenses()
            exp.user = request.user
            exp.category=exp_form.cleaned_data['category']
            exp.purpose = exp_form.cleaned_data['purpose']
            exp.amount = exp_form.cleaned_data['amount']
            exp.save()
        return redirect('show')

    else:
        exp_form = MyExpenses(request.user)
        exp_form.user=request.user
        contex = {
            'exp_form':exp_form
        }
    return render(request, 'form.html', contex)


def add_category(request):
    if request.method == 'POST':
        category = Add_category(request.POST)
        if category.is_valid():
            ct = Category.objects.all()
            cat = Category()
            cat.user = request.user
            cat.category = category.cleaned_data['category']
            for i in ct:
                if i.category == cat.category and i.user==request.user:
                    return redirect('/')
            cat.save()
            return redirect('add')
    else:
        category = Add_category()
    return render(request, 'form.html', {'category': category})


@login_required(login_url='login')
def show_catg(request):
    cur_user = request.user
    catgs = Category.objects.filter(user=cur_user)
    return render(request, 'base.html', {'catgs': catgs})

def edit(request, id):
    expense = Expenses.objects.get(id=id)
    if request.method == 'POST':
        expe=MyExpenses(request.POST,instance=expense)
        if expe.is_valid():
            expe.save()
            return redirect('data')
    else:
        form = MyExpenses(instance=expense, user=request.user)
        contex = {
            'form':form
        }
    return render(request, 'edit.html', contex)
    
def delete(request, id):
    expense = Expenses.objects.get(id=id)
    expense.delete()
    return redirect('data')
