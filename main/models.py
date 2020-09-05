from django.db import models

# Create your models here.
class Expenses(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=200)
    amount = models.IntegerField()
    
    def __str__(self):
        return self.purpose
    