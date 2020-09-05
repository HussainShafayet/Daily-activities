from django import forms
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class Register(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2'
            
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':'First name','label':''})
        }

class Login(AuthenticationForm):
    class Meta:
        model = AuthenticationForm
        fields = [
            'email','password'
        ]
