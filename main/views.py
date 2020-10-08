from django.shortcuts import render,redirect
from .models import Expenses, Category, User
from .forms import MyExpenses, Register, UserLoginForm,Add_category
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages



# Create your views here.
def register(request):
    if request.method == "POST":
        user_form = Register(request.POST)
        if user_form.is_valid():
            all_email = User.objects.values_list('email',flat=True)
            user_email = user_form.cleaned_data['email']
            for i in all_email:
                if i == user_email:
                    messages.error(request,'Email Already added')
                    return render(request,'register.html',{'user_form':user_form})
            user_form.save() 
            messages.success(request, 'Registration Successful')
            return redirect('login')        
    else:
       
        user_form = Register()
    contex = {
            'user_form': user_form
            }
    return render(request, 'register.html',contex)


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
    else:
        log_form = UserLoginForm()
        contex = {'log_form': log_form}
    return render(request, 'login.html', contex)

def logout(request):
    django_logout(request)
    return redirect('main')


def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def data(request):
    current_user = request.user
    catgs = Category.objects.filter(user=current_user)
    if request.POST.get('categ'):
        cat = request.POST.get('categ')
        if cat == 'All':
            catgs = Category.objects.filter(user=current_user)
            exps = Expenses.objects.filter(
            user=current_user).order_by('category', 'date',)
            total_exps = exps.aggregate(Sum('amount'))
            context = {
                'cat':cat,
                'catgs': catgs,
                'total_exps': total_exps,
                'exps': exps
            }
            return render(request, 'data.html', context)

        else:
            id = Category.objects.get(user=current_user,category=cat)
            exps = Expenses.objects.filter(user=current_user, category=id).order_by('date')
            total_exps = exps.aggregate(Sum('amount'))
            context = {
                'cat':cat,
                'catgs': catgs,
                'total_exps': total_exps,
                'exps': exps
            }
            return render(request, 'data.html', context)
    else:
        catgs = Category.objects.filter(user=current_user)
        exps = Expenses.objects.filter(user=current_user).order_by('category','date',)
        total_exps = exps.aggregate(Sum('amount'))
        context = {
            'catgs': catgs,
            'total_exps': total_exps,
            'exps': exps
        }
        return render(request, 'data.html', context)


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
        return redirect('data')

    else:
        exp_form = MyExpenses(request.user)
        exp_form.user=request.user
        contex = {
            'exp_form':exp_form
        }
    return render(request, 'form.html', contex)


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        category = Add_category(request.POST)
        if category.is_valid():
            all_cat = Category.objects.all()
            cat = Category()
            cat.user = request.user
            cat.category = category.cleaned_data['category']
            for i in all_cat:
                if i.category == cat.category and i.user == request.user:
                    contex = {
                        'category': Add_category(),
                        'error':'This category already added!'
                    }
                    return render(request, 'category.html', contex)
            cat.save()
            return redirect('add')
    else:
        category = Add_category()
        contex = {
            'category': category
        }
    return render(request, 'category.html', contex)


@login_required(login_url='login')
def show_catg(request):
    cur_user = request.user
    catgs = Category.objects.filter(user=cur_user)
    return render(request, 'data.html', {'catgs': catgs})

def edit(request, id):
    expense = Expenses.objects.get(id=id)
    if request.method == 'POST':
        expense.category=Category.objects.get(id=request.POST['category'])
        expense.purpose=request.POST['purpose']
        expense.amount=request.POST['amount']
        expense.save()
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
