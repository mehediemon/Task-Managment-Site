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
    description = models.CharField(max_length=500, null=True)
    file = models.FileField(upload_to='documetns/')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    
    name = models.CharField(max_length=500,)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS, default='0')
    time = models.FloatField()

    def __str__(self) -> str:
        return self.name
    



# Create your models here.
