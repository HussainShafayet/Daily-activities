from django.shortcuts import render,redirect
from .models import Expenses, Category,Profile, User
from .forms import MyExpenses, Register, UserLoginForm, Add_category, UserProfileForm,ProfileForm
from django.contrib.auth.views import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage



# Create your views here.
def register(request):
    if request.method == "POST":
        user_form = Register(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
       
        user_form = Register()
    contex = {
            'user_form': user_form
            }
    return render(request, 'register.html',contex)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def user_login(request):
    if request.method == 'POST':
        log_form = UserLoginForm(request.POST)
        if log_form.is_valid():
            username = log_form.cleaned_data['username']
            password = log_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Login Successfully')
                return redirect('/')
            else:
                messages.error(request,'Try again')
                contex = {
                    'log_form':UserLoginForm(),
                    'error': 'Username or Password Incorrect'
                    
                }
                return render(request,'login.html',contex)
    else:
        log_form = UserLoginForm()
        contex = {'log_form': log_form}
    return render(request, 'login.html', contex)



def user_logout(request):
    logout(request)
    messages.warning(request,'You are logged out')
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
@login_required(login_url='login')
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
@login_required(login_url='login')  
def delete(request, id):
    expense = Expenses.objects.get(id=id)
    expense.delete()
    return redirect('data')
@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        pro_form = ProfileForm(request.POST, request.FILES or None)
        if pro_form.is_valid():
            pro = Profile()
            pro.user = request.user
            pro.image=pro_form.cleaned_data['image']
            #pro.file=pro_form.cleaned_data['file']
            pro.save()
            return redirect('profile')
    else:
        pro_form=ProfileForm()
    return render(request, 'profile.html', {'pro_form': pro_form})


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile update success')
            return redirect('profile')
        else:
            messages.error(request, 'Try again')
            return redirect('edit-profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request,'profile-edit.html',{'form':form})
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password change successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Try again')
            return redirect('password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change-password.html', {'form': form})
