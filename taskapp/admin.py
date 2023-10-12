from django.contrib import admin
from taskapp.models import Task, Client, Type, Document

admin.site.register(Task)
admin.site.register(Client)
admin.site.register(Type)
admin.site.register(Document)
# Register your models here.
