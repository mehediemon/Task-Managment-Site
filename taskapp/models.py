from django.db import models
from django.contrib.auth.models import User


STATUS = (
        ('0', 'Pending'),
        ('1', 'Completed')
    )

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    
    name = models.CharField(max_length=500,)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS, default='0')
    time = models.FloatField()

    def __str__(self) -> str:
        return self.name
    

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
