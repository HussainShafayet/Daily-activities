from django.shortcuts import render,redirect
from .models import Expenses
from .forms import MyExpenses
from django.contrib import messages


# Create your views here.
def main(request):
    return render(request,'main.html')
def data(request):
    exps = Expenses.objects.all()
    return render(request, 'data.html', {'exps':exps})

def form(request):
    if request.method == 'POST':
        exp_form = MyExpenses(request.POST)
        if exp_form.is_valid():
            exp_form.save()
        return redirect('main')
    else:
        exp_form = MyExpenses()
        return render(request, 'form.html', {'exp_form': exp_form})


    

