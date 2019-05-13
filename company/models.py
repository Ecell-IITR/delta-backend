from django.db import models
from users.models.user import User

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

def __str__(self):
    return str(self.user)