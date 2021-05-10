from django import forms
from .import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Expenses, Category, Profile, ExpensesTitle
from django.core.validators import validate_email


class Expenses_Title_Form(forms.ModelForm):
    class Meta:
        model = ExpensesTitle
        fields = [
            'title'
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(Expenses_Title_Form,self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(Expenses_Title_Form, self).clean()
        title = cleaned_data.get("title")

        if ExpensesTitle.objects.filter(title=title, user=self.user):
            raise forms.ValidationError('Title name already exists.')
        return self.cleaned_data


class MyExpenses(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = [
            'category', 'purpose', 'amount'
        ]

    def __init__(self, user, *args, **kwargs):
        super(MyExpenses, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


class Add_category(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'title','category'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(Add_category, self).__init__(*args, **kwargs)
        
    def clean(self):

        cleaned_data = super(Add_category, self).clean()
        category = cleaned_data.get("category")
        title=cleaned_data.get('title')

        if Category.objects.filter(category=category,user=self.user,title=title):
            raise forms.ValidationError('Category already exists.')
        return self.cleaned_data


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2'

        ]
        labels = {
            'email': 'Email*'
        }

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'autofocus': True,
            'required': True,
            'placeholder': 'First name',
        })
        self.fields['last_name'].widget.attrs.update({
            'required': True,
            'placeholder': 'Last name'
        })
        self.fields['username'].widget.attrs.update({
            'placeholder': 'username',
            'autofocus': False
        })
        self.fields['email'].widget.attrs.update({
            'required': True,
            'placeholder': 'Email',

        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password'
        })

    """ def clean(self):
        cleaned_data = super(Register, self).clean()
        email = cleaned_data.get("email")
        
        if User.objects.filter(email=email):
            raise forms.ValidationError('Email already exists.')
        return self.cleaned_data """


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    password = None

    class Meta:
        model = User

        fields = [
            'first_name', 'last_name', 'username', 'email'
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image'
        ]
