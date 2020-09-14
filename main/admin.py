from django.contrib import admin
from .models import Expenses,Category

# Register your models here.
admin.site.register(Expenses)
admin.site.register(Category)