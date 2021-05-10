from django.contrib import admin
from .models import Expenses,Category,Profile,ExpensesTitle

# Register your models here.
admin.site.register(ExpensesTitle)
admin.site.register(Expenses)
admin.site.register(Category)
admin.site.register(Profile)