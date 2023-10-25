from django.contrib import admin
from taskapp.models import Task, Client, Type, CustomUser

admin.site.register(Task)
admin.site.register(Client)
admin.site.register(Type)
admin.site.register(CustomUser)

# Register your models here.
