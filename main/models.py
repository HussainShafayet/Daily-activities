from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/', default='/images/profile.png')
    #file=models.FileField(null=True,blank=True,upload_to='documents/')
    
class ExpensesTitle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title

class Category(models.Model):
    title=models.ForeignKey(ExpensesTitle,on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.category

class Expenses(models.Model):
    title = models.ForeignKey(ExpensesTitle, on_delete=models.CASCADE,)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    purpose = models.CharField(max_length=200)
    amount = models.IntegerField()
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.purpose
