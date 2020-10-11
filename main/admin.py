from django.contrib import admin
from .models import Expenses,Category,Profile

# Register your models here.
admin.site.register(Expenses)
admin.site.register(Category)
admin.site.register(Profile)