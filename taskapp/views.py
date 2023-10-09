from django.shortcuts import render, redirect
from taskapp.models import Task, Client
from django.contrib.auth.models import User

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
    clients = Client.objects.all()
    print(clients)
    if request.method == 'POST':
        task = request.POST['task']
        client = request.POST['client']
        client = Client.objects.get(id=client)
        date = request.POST['date']
        type = request.POST['type']
        status = request.POST['status']
        time = request.POST['time']
        Task.objects.create(name=task, client=client, date=date, type=type, status=status, time=time)
        return redirect('home')
       

    return render(request, "add_task.html", { "clients" : clients })

def edit_task(request, task_id):
    print(task_id)
    task = Task.objects.get(id=task_id)
    
    task_name = request.GET.get('task_name')
    if task_name:
        task.name = task_name
        task.time = request.GET.get('time')
        task.status = request.GET.get('status')
        task.save()
        return redirect('home')
 
    return render(request, "edit_task.html", { "task" : task})


def main(request):
    return render(request, "main.html")

def signup(request):
    return render(request, "signup.html")