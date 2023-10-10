from django.shortcuts import render, redirect
from taskapp.models import Task, Client, Type
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
    typeall = Type.objects.all()
    userall = User.objects.all()
    print(userall)
    print(typeall)
    print(clients)
    if request.method == 'POST':
        task = request.POST['task']
        client = request.POST['client']
        client = Client.objects.get(id=client)
        date = request.POST['date']
        type = request.POST['type']
        type = Type.objects.get(id=type)
        status = request.POST['status']
        time = request.POST['time']
        user = request.POST['user']
        print(user)
        user = User.objects.get(id=user)
        Task.objects.create(name=task, client=client, date=date, type=type, status=status, time=time, user=user)
        return redirect('home')
       

    return render(request, "add_task.html", { "clients" : clients, "type": typeall, "userl": userall })

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

    if request.method == 'POST':
     fname = request.POST['fname']
     lname = request.POST['lname']
     username = request.POST['username']
     email = request.POST['email']
     password = request.POST['pass1']

     myuser = User.objects.create_user(username=username, email=email, password=password)   
     myuser.first_name = fname
     myuser.last_name = lname
     myuser.save()


    return render(request, "signup.html")