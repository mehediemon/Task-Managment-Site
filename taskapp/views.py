from django.shortcuts import render, redirect
from taskapp.models import Task, Client, Type, Document
from taskapp.forms import DocumentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
@login_required(login_url="/accounts/login/")
def home(request):
    docs = Document.objects.all()
    userall = User.objects.get(id=request.user.id)
    taskf = Task.objects.filter(user=userall)
    all_tasks = Task.objects.all()
    if request.method == 'POST':
        print("view")
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()

    return render(request, "home.html", {
        "all_tasks" : all_tasks, "taskfl": taskf, "form" : form, "docs" : docs
    })




@login_required(login_url="/accounts/login/")
def completed_task(request):
    userall = User.objects.get(id=request.user.id)
    print(userall)
    completed_tasks = Task.objects.filter(user=userall, status="1")

    return render(request, "completed_task.html", {
        "completed_tasks" : completed_tasks 
    })
@login_required
def pending_task(request):
    userall = User.objects.get(id=request.user.id)
    pending_tasks = Task.objects.filter(user=userall, status="0")

    return render(request, "pending.html", {
        "pending_tasks" : pending_tasks 
    })

@login_required
def add_task(request):
    clients = Client.objects.all()
    typeall = Type.objects.all()
    userall = User.objects.get(id=request.user.id)
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
        user = User.objects.get(id=user)
        Task.objects.create(name=task, client=client, date=date, type=type, status=status, time=time, user=user)
        return redirect('home')
       

    return render(request, "add_task.html", { "clients" : clients, "type": typeall, "userl": userall })


@login_required
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

@login_required
def main(request):
    return render(request, "main.html")


def signup(request):
    if request.method == 'POST':
     fname = request.POST['fname']
     lname = request.POST['lname']
     username = request.POST['username']
     email = request.POST['email']
     password = request.POST['pass1']
     password2 = request.POST['pass2']
     if password == password2:
        myuser = User.objects.create_user(username=username, email=email, password=password)   
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
    else:
        print("password not matched")

     


    return render(request, "signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            print("no user matched")

    return render(request, "signin.html")




def logout_view(request):
    logout(request)
    return redirect("signin")