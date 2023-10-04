from django.db import models


STATUS = (
        ('0', 'Pending'),
        ('1', 'Completed')
    )

class Task(models.Model):
    
    name = models.CharField(max_length=500,)
    type = models.CharField(max_length=100, null=True, blank=True, )
    client = models.CharField(max_length=255,)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS, default='0')
    time = models.FloatField()

    def __str__(self) -> str:
        return self.name


# Create your models here.
