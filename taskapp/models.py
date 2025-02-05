from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('general', 'General'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='general')

    def __str__(self):
        return self.username
    

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


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
    description = models.TextField(max_length=500, null=True)
    file = models.FileField(upload_to='documents/')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    PRIORITY = (
        ('0', 'low'),
        ('1', 'medium'),
        ('2', 'high')
    )    
    name = models.CharField(max_length=500,)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='assigned_user')
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date = models.DateField()
    priority = models.CharField(max_length=12, choices=PRIORITY, default='low', null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='0')
    time = models.FloatField()

    def get_priority_display_value(self):
        for value, label in self.PRIORITY:
            if value == self.priority:
                return label
        return None

    def __str__(self) -> str:
        return self.name
    



# Create your models here.
