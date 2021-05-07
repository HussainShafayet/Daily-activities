from django.shortcuts import render, redirect
from .models import Expenses, Category, Profile, User
from .forms import MyExpenses, Register, UserLoginForm, Add_category, UserProfileForm, ProfileForm
from django.contrib.auth.views import PasswordChangeForm, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import UserPassesTestMixin
from Daily_activities.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

from django.db.models import Q

import json
from django.http import JsonResponse


# Create your views here.


def register(request):
    if request.method == "POST":
        user_form = Register(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            new_profile = Profile(user=user)
            new_profile.save()
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
            context = {
                'user_form': user_form
            }
            return render(request, 'register.html', context)

    else:
        user_form = Register()
        context = {
            'user_form': user_form
        }
    return render(request, 'register.html', context)


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
                messages.error(request, 'Try again')
                context = {
                    'log_form': UserLoginForm(),
                    'error': 'Username or Password Incorrect'

                }
                return render(request, 'login.html', context)
    else:
        log_form = UserLoginForm()
        context = {'log_form': log_form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return redirect('main')


def main(request):
    return render(request, 'main.html')


def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')
def data(request):
    current_user = request.user
    catgs = Category.objects.filter(user=current_user)
    if ('search') in request.GET:
        cat = request.GET.get('search')
        if cat:
            catgs = Category.objects.filter(user=current_user).filter(
                Q(category__icontains=str(cat)))
            if catgs:
                test = []
                for i in catgs:
                    expen = Expenses.objects.filter(
                        user=current_user, category=i).order_by('date')
                    for j in expen:
                        test.append(j)
                if not test:
                    context = {
                        'message': 'Not found.'
                    }
                    return render(request, 'data.html', context)
                amount = 0
                for i in test:
                    amount = amount + (i.amount)
                val = 'amount'
                context = {
                    'cat': cat,
                    'catgs': catgs,
                    'total_exps': amount,
                    'exps': test,
                    'val': val,
                }
                return render(request, 'data.html', context)
            else:
                exps = Expenses.objects.filter(user=current_user).filter(
                    Q(purpose__icontains=str(cat)) | Q(amount__icontains=str(cat)) | Q(date__icontains=str(cat)))
                if not exps:
                    context = {
                        'message': 'Not found.'
                    }
                    return render(request, 'data.html', context)
                total_exps = exps.aggregate(Sum('amount'))
                context = {
                    'cat': cat,
                    'catgs': catgs,
                    'total_exps': total_exps,
                    'exps': exps
                }
                return render(request, 'data.html', context)
        else:
            catgs = Category.objects.filter(user=current_user)
            exps = Expenses.objects.filter(
                user=current_user).order_by('category', 'date',)
            total_exps = exps.aggregate(Sum('amount'))
            context = {
                'catgs': catgs,
                'total_exps': total_exps,
                'exps': exps
            }
            return render(request, 'data.html', context)

    else:
        catgs = Category.objects.filter(user=current_user)
        exps = Expenses.objects.filter(
            user=current_user).order_by('category', 'date',)
        total_exps = exps.aggregate(Sum('amount'))
        context = {
            'catgs': catgs,
            'total_exps': total_exps,
            'exps': exps
        }
        return render(request, 'data.html', context)


def search_item(request):
    if request.method == "POST":
        current_user = request.user
        search_str = json.loads(request.body).get("searchText")
        catg = Category.objects.filter(user=current_user).filter(
            Q(category__icontains=str(search_str)))
        test = []
        for i in catg:
            expen = Expenses.objects.filter(
                user=current_user, category=i).order_by('date')
            for j in expen:
                test.append(j)
        amount = 0
        for i in test:
            amount = amount + (i.amount)

        #data = test.values()
        # print(data)
        return JsonResponse(expen, safe=False)


@login_required(login_url='login')
def form(request):
    if request.method == 'POST':
        exp_form = MyExpenses(request.user, request.POST)
        if exp_form.is_valid():
            exp = Expenses()
            exp.user = request.user
            exp.category = exp_form.cleaned_data['category']
            exp.purpose = exp_form.cleaned_data['purpose']
            exp.amount = exp_form.cleaned_data['amount']
            exp.save()
            messages.success(request, 'Added Successfully.')
            return redirect('data')
        else:
            messages.warning(request, 'Try again!')
            context = {
                'exp_form': exp_form
            }
        return render(request, 'form.html', context)

    else:
        exp_form = MyExpenses(request.user)
        exp_form.user = request.user
        context = {
            'exp_form': exp_form
        }
    return render(request, 'form.html', context)


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
                    messages.warning(request, 'This category already added!')
                    return redirect('category')
            cat.save()
            messages.success(request, 'Category added successfully.')
            return redirect('add')
        else:
            context = {
                'category': category
            }
        return render(request, 'category.html', context)
    else:
        category = Add_category()
        context = {
            'category': category
        }
    return render(request, 'category.html', context)


@login_required(login_url='login')
def show_catg(request):
    cur_user = request.user
    catgs = Category.objects.filter(user=cur_user)
    return render(request, 'data.html', {'catgs': catgs})


@login_required(login_url='login')
def edit(request, id):
    expense = Expenses.objects.get(id=id)
    if request.method == 'POST':
        expense.category = Category.objects.get(id=request.POST['category'])
        expense.purpose = request.POST['purpose']
        expense.amount = request.POST['amount']
        expense.save()
        messages.success(request, 'Update successfully.')
        return redirect('data')
    else:
        form = MyExpenses(instance=expense, user=request.user)
        context = {
            'form': form
        }
    return render(request, 'edit.html', context)


@login_required(login_url='login')
def delete(request, id):
    expense = Expenses.objects.get(id=id)
    expense.delete()
    messages.success(request, 'Deleted Successfully.')
    return redirect('data')


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        pro_form = ProfileForm(request.POST, request.FILES or None)
        if pro_form.is_valid():
            pro = Profile()
            pro.user = request.user
            pro.image = pro_form.cleaned_data['image']
            pro.save()
            return redirect('profile')
    else:
        pro_form = ProfileForm()
    return render(request, 'profile.html', {'pro_form': pro_form, 'profile_details': 'profile_details'})


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        form2 = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if form.is_valid() and form2.is_valid():
            form.save()
            profile = Profile.objects.get(user=request.user)
            image = profile.image
            if str(image) in '/images/profile.png':
                form2.save()
                messages.success(request, 'Profile update success')
                return redirect('profile')
            else:
                image.delete()
                form2.save()
                messages.success(request, 'Profile update success')
                return redirect('profile')
        else:
            messages.warning(request, 'Try again')
            context = {
                'form': form,
                'form2': form2

            }
            return render(request, 'profile.html', context)
    else:
        form = UserProfileForm(instance=request.user)
        form2 = ProfileForm()
        context = {
            'form': form,
            'form2': form2

        }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password change successfully!')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else:
            messages.error(request, 'Try again')
            return redirect('password')
    else:
        form = PasswordChangeForm(user=request.user)
        val = 'password_change'
        context = {
            'form': form,
            'val': val,
        }
    return render(request, 'profile.html', context)


class ResetPassword(UserPassesTestMixin, PasswordResetView):
    template_name = 'password_reset.html'

    def test_func(self):
        return self.request.user.is_anonymous


class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class ResetPasswordComplete(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
