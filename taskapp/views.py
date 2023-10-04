from django.shortcuts import render
from taskapp.models import Task

# Create your views here.
def home(request):
    all_tasks = Task.objects.all()

    return render(request, "home.html", {
        "all_tasks" : all_tasks 
    })

def completed_task(request):
    completed_tasks = Task.objects.filter(status="1")

    return render(request, "completed_task.html", {
        "completed_tasks" : completed_tasks 
    })

def pending_task(request):
    pending_tasks = Task.objects.filter(status="0")

    return render(request, "pending.html", {
        "pending_tasks" : pending_tasks 
    })
def add_task(request):
    return render(request, "add_task.html")