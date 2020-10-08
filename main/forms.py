from django import forms
from .import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expenses,Category

class MyExpenses(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = [
            'category','purpose','amount'
        ]

    def __init__(self, user, *args, **kwargs):
        super(MyExpenses,self).__init__(*args, **kwargs)
        self.fields['category'].queryset=Category.objects.filter(user=user)


class Add_category(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'category'
        ]
        widgets = {
        'name': forms.TextInput(attrs={'placeholder':'Enter category'})
        }
class Register(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2'

        ]
        labels = {
            'email':'Email*'
        }
    def __init__(self,*args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs.update({
            'autofocus': True,
            'required':True,
            'placeholder': 'First name',
        })
        self.fields['last_name'].widget.attrs.update({
            'required': True,
            'placeholder': 'Last name'
        })
        self.fields['username'].widget.attrs.update({
            'placeholder': 'username',
            'autofocus':False
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

        


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    
