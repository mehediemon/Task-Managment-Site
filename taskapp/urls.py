from django.urls import path, include
from taskapp.views import completed_task, home, pending_task, add_task

urlpatterns = [
    path('', home, name="home"),
    path('completed-task/', completed_task, name="completed_task"),
    path('pending-task/', pending_task, name="pending_task"),
    path('add-task/', add_task, name="add_task")
]