from django import forms
from . import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MyExpenses(forms.ModelForm):
    class Meta:
        model = models.Expenses
        fields = "__all__"


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2'

        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'label': ''})
        }



class UserLoginForm(forms.Form):
    username = forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    
