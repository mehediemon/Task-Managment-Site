from django.contrib import admin
from taskapp.models import Task, Client, Type

admin.site.register(Task)
admin.site.register(Client)
admin.site.register(Type)

# Register your models here.
