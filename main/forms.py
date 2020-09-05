from django import forms
from . import models
from django.forms import ModelForm


class MyExpenses(forms.ModelForm):
    class Meta:
        model = models.Expenses
        fields ="__all__"

