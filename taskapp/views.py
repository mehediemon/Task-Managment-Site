from django.shortcuts import render, redirect
from django.http import JsonResponse
from taskapp.models import Task, Client, Type
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from datetime import *
from django.utils import timezone
import os

# Create your views here.
@login_required(login_url="/login/")
def home(request):
    daten = date.today()
    docs = Client.objects.all()
    cnum = Client.objects.all().count()
    userall = User.objects.get(id=request.user.id)
    taskf = Task.objects.filter(user=userall, date=daten)
    total_task = Task.objects.filter(user=userall, status="0").count()
    total_ctask = Task.objects.filter(user=userall, status="1").count()
    all_tasks = Task.objects.all()

    return render(request, "home.html", {
        "all_tasks" : all_tasks, "taskfl": taskf, "docs" : docs, "user" : userall, "count" : total_task, "clnum" : cnum, "complete_task" : total_ctask
    })




@login_required(login_url="/login/")
def completed_task(request):
    userall = User.objects.get(id=request.user.id)
    print(userall)
    completed_tasks = Task.objects.filter(user=userall, status="1")

    return render(request, "completed_task.html", {
        "completed_tasks" : completed_tasks 
    })
@login_required(login_url="/login/")
def pending_task(request):
    userall = User.objects.get(id=request.user.id)
    pending_tasks = Task.objects.filter(user=userall, status="0")

    return render(request, "pending.html", {
        "pending_tasks" : pending_tasks 
    })


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def add_client(request):
    daten = date.today()
    docs = Client.objects.all()
    userall = User.objects.get(id=request.user.id)
    taskf = Task.objects.filter(user=userall, date=daten)
    total_task = Task.objects.filter(user=userall, status="0").count()
    all_tasks = Task.objects.all()
    client_list = Client.objects.all()

    if request.method == 'POST' and request.FILES.get('file'):

        
        name = request.POST['name']
        description = request.POST['description']
        try:
            client = Client.objects.get(name=name)
            error_message = "A client with the same name already exists. Please choose a different name."
            return render(request, "client_list.html", {
                "all_tasks" : all_tasks, "taskfl": taskf, "docs" : docs, "user" : userall, "count" : total_task, "error_client" : error_message
                })
        except Client.DoesNotExist:
            uploaded_file = request.FILES['file']
            original_filename = uploaded_file.name

            new_file = Client(name=name, file=uploaded_file, original_filename=original_filename, description=description)

            # Generate a unique filename based on the current timestamp
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            file_extension = os.path.splitext(original_filename)[-1]
            new_filename = f"{timestamp}{file_extension}"

            # Rename the file and save it
            new_file.file.name = os.path.join('client_Files', new_filename)
            new_file.save()

            return redirect('add_client')


    return render(request, "client_list.html", {"docs" : docs} )

@login_required(login_url="/login/")
def get_task_details(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task_data = {
            'id': task.id,
            'name': task.name,
            'client': task.client.name,
            'date': str(task.date),
            'status': task.status,
            'type': task.type.id,  # Replace with the appropriate type field
            'time': task.time,
        }
        return JsonResponse(task_data)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    
@login_required(login_url="/login/")
def get_client_data(request, client_id):
    try:
        clients = Client.objects.get(pk=client_id)
        # Prepare a dictionary with task information
        client_data = {
            'name': clients.name,
            'description': clients.description,
            'file_url': clients.file.url,
            'filename': clients.original_filename,
        }
        return JsonResponse(client_data)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'})
    

def logout_view(request):
    logout(request)
    return redirect("signin")



@login_required(login_url="/login/")
@csrf_exempt
def update_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.name = request.POST.get('task_name', task.name)
            task.client = request.POST.get('client_name', task.client)
            task.date = request.POST.get('date', task.date)
            task.status = request.POST.get('status', task.status)
            task.type = request.POST.get('type', task.type)
            task.time = request.POST.get('time', task.time)
            task.save()
            return JsonResponse({'message': 'Task updated successfully'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)