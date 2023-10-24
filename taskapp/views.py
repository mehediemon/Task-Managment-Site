from django.shortcuts import get_object_or_404, render, redirect
import xlsxwriter
from django.http import HttpResponse
from django.http import JsonResponse
from taskapp.models import Task, Client, Type
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import *
from datetime import date
from django.utils import timezone
import os

# permission for admin
def is_admin(user):
    # Customize this function to match your role check logic
    return user.is_authenticated and user.role == 'admin'

admin_required = user_passes_test(is_admin, login_url='home')


# Create your views here.
# Home view
@login_required(login_url="/login/")
def home(request):
    daten = date.today()
    docs = Client.objects.all()
    cnum = Client.objects.all().count()
    users = CustomUser.objects.all()
    login_user = CustomUser.objects.get(id=request.user.id)
    if request.user.is_superuser:
        taskf = Task.objects.all()
        total_task = Task.objects.filter(status="0").count()
        total_ctask = Task.objects.filter(status="1").count()
        all_tasks = Task.objects.filter(status="0").order_by('-priority')
    else:
        taskf = Task.objects.filter(user=login_user, date=daten)
        total_task = Task.objects.filter(assigned_user=login_user, status="0").count()
        total_ctask = Task.objects.filter(assigned_user=login_user, status="1").count()
        all_tasks = Task.objects.filter(assigned_user=login_user, status="0").order_by('-priority')

    return render(request, "home.html", {
        "all_tasks" : all_tasks, "taskfl": taskf, "docs" : docs, "user" : login_user, "count" : total_task, "clnum" : cnum, "complete_task" : total_ctask, "users" : users
    })



# For task that is already completed
@login_required(login_url="/login/")
def completed_task(request):
    userall = CustomUser.objects.get(id=request.user.id)
    print(userall)
    if request.user.is_superuser:
        completed_tasks = Task.objects.filter(status="1")
    else:
        completed_tasks = Task.objects.filter(assigned_user=userall, status="1")


    return render(request, "completed_task.html", {
        "completed_tasks" : completed_tasks 
    })


# For Pending tasks
@login_required(login_url="/login/")
def pending_task(request):
    users = CustomUser.objects.all()
    if request.user.is_superuser:
        pending_tasks = Task.objects.filter(status="0").order_by('created_at')
    else:
        userall = CustomUser.objects.get(id=request.user.id)
        pending_tasks = Task.objects.filter(assigned_user=userall, status="0").order_by('created_at')
    return render(request, "pending.html", {
        "pending_tasks" : pending_tasks , "users" : users
    })



# For Adding Task
@login_required(login_url="/login/")
def add_task(request):
    clients = Client.objects.all()
    typeall = Type.objects.all()
    userall = CustomUser.objects.all()
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        task = request.POST['task']
        client = request.POST['client']
        client = Client.objects.get(id=client)
        date = request.POST['date']
        type = request.POST['type']
        type = Type.objects.get(id=type)
        status = request.POST['status']
        priority = request.POST['priority']
        time = request.POST['time']
        user = request.POST['user']
        user = CustomUser.objects.get(id=user)
        init_user = CustomUser.objects.get(id=request.user.id)
        Task.objects.create(name=task, client=client, date=date, type=type, status=status, time=time, user=init_user, priority=priority, assigned_user=user)
        return redirect('home')
       

    return render(request, "add_task.html", { "clients" : clients, "type": typeall, "userl": userall })


#

@login_required(login_url="/login/")
@admin_required
def edit_task(request):
    users = CustomUser.objects.all()
    print(users)
    return render(request, "user_list.html", { "users" : users})




@login_required(login_url="/login/")
def main(request):
    return render(request, "main.html")


# For User SignUP

def signup(request):
    if request.method == 'POST':
     fname = request.POST['fname']
     lname = request.POST['lname']
     username = request.POST['username']
     email = request.POST['email']
     password = request.POST['pass1']
     password2 = request.POST['pass2']
     role = request.POST.get('role', 'general')
     if password == password2:
        try:
            usere = CustomUser.objects.get(username=username)
            messages.error(request, "Client name alrady exist")
            return render(request, "signup.html")
        except CustomUser.DoesNotExist:
            myuser = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)   
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            return redirect("signin")
    else:
        print("password not matched")

    return render(request, "signup.html")


# For Log in

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
            messages.error(request, "username or password not matched")

    return render(request, "signin.html")



# For Add Client

@login_required(login_url="/login/")
def add_client(request):
    daten = date.today()
    docs = Client.objects.all().order_by('-id')
    userall = CustomUser.objects.get(id=request.user.id)
    client_list = Client.objects.all()
    cnum = Client.objects.all().count()
    if request.user.is_authenticated and request.user.role == 'admin':

        if request.method == 'POST' and request.FILES.get('file'):

        
            name = request.POST['name']
            description = request.POST['description']
            try:
                client = Client.objects.get(name=name)
                print(client.uploaded_at)
                messages.error(request, "Client name alrady exist")
                return render(request, "client_list.html", {
                    "docs" : docs, "user" : userall, "clnum" : cnum
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
    else:
        messages.error(request, "You do not have permission.")
        

    return render(request, "client_list.html", {
        "docs" : docs, "clnum" : cnum, "user" : userall
        } )



# For viewing Client Data in modal

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


# For viewing Pending task in Modal

@login_required(login_url="/login/")
def get_task_details(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task_data = {
            'id': task.id,
            'name': task.name,
            'user': task.user.username,
            'assigned_user' : task.assigned_user.username,
            'assigned_user_id' : task.assigned_user.id,
            'client': task.client.name,
            'fdate': str(task.date),
            'date': str(task.created_at),
            'status': task.status,
            'type': task.type.name,  # Replace with the appropriate type field
            'time': task.time,
        }
        return JsonResponse(task_data)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)






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
            task.time = request.POST.get('time', task.time)
            user_id = request.POST.get('assign_user')
            assigned_user = get_object_or_404(CustomUser, id=user_id)
            task.assigned_user = assigned_user
            task.save()
            return JsonResponse({'message': 'Task updated successfully'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

@login_required(login_url="/login/")
def download_excel(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Validate and parse the date strings into datetime objects
    try:
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
    except (ValueError, TypeError):
        # Handle invalid dates, e.g., return an error response
        return HttpResponse("Invalid date parameters", status=400)



    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="task_list.xlsx"'

    # Create an Excel workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    headers = ['Date', 'Finish Date', 'Task', 'Time', 'Done By']  # Add more headers as needed

    # Write column headers to the worksheet.
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Write your task data to the worksheet.
    # For example, if you have a queryset 'tasks', you can loop through it and write data to the worksheet.
    #tasks = Task.objects.all()
    userall = CustomUser.objects.get(id=request.user.id)
    if request.user.is_superuser:
        tasks = Task.objects.filter(status="1", date__range=(start_date, end_date))
    else:
        tasks = Task.objects.filter(assigned_user=userall, status="1", date__range=(start_date, end_date))

    row = 1
    for task in tasks:
        userall = CustomUser.objects.get(id=request.user.id)
        formatted_date = task.created_at.strftime('%m/%d/%Y')
        finish_date = task.date.strftime('%m/%d/%Y')
        worksheet.write(row, 0, formatted_date)
        worksheet.write(row, 1, finish_date)
        worksheet.write(row, 2, task.name)
        worksheet.write(row, 3, task.time)
        worksheet.write(row, 4, task.assigned_user.username)

        # Add more fields as needed
        row += 1

    workbook.close()
    return response


@login_required(login_url="/login/")
def edit_user(request, user_id):
    loged_test = request.user.username
    loged_role = request.user.role
    user = CustomUser.objects.get(id=user_id)
    print(user)
    
    if request.user.is_authenticated and request.user.is_superuser:
        print("inside")
        username = request.GET.get('user_name')
        if username:
            print("inside 2")
            pass1 = request.GET.get('password')
            print(pass1)
            pass2 = request.GET.get('password2')
            if pass1 == "" and pass2 == "":
                user.first_name = request.GET.get('first_name')
                user.last_name = request.GET.get('last_name')
                user.email = request.GET.get('email')
                user.role = request.GET.get('role')
                print("null pass")
                user.save()
                messages.error(request, "user info changed")
            elif pass1 != "" and pass1 == pass2:
                user.first_name = request.GET.get('first_name')
                user.last_name = request.GET.get('last_name')
                user.email = request.GET.get('email')
                user.role = request.GET.get('role')
                print(" with pass")
                user.set_password(pass1)
                user.save()
                messages.error(request, "password changed")
            else:
                messages.error(request, "password fields not same.")

            return redirect('edit_task')
    else:
        messages.error(request, "not permitted")

    return render(request, 'edit_user.html', {'user': user, 'loged_user' : loged_test, "loged_role" : loged_role})


@login_required(login_url="/login/")
def edit_own_profile(request):
        loged_test = request.user.username
        user = CustomUser.objects.get(id=request.user.id)
        print(user)
        if request.user.is_authenticated:
            username = request.GET.get('user_name')
            pass1 = request.GET.get('password')
            pass2 = request.GET.get('password2')
            print(username)

            if username:

                if pass1 == "" and pass2 == "":
                    user.first_name = request.GET.get('first_name')
                    user.last_name = request.GET.get('last_name')
                    user.email = request.GET.get('email')
                    user.save()
                    messages.error(request, "user info changed.")
                elif pass1 != "" and pass1 == pass2:
                    user.first_name = request.GET.get('first_name')
                    user.last_name = request.GET.get('last_name')
                    user.email = request.GET.get('email')
                    user.set_password(pass1)
                    user.save()
                    messages.success(request, "password changed.")
                else:
                    messages.error(request, "password fields not same.")
                    
            
        return render(request, 'edit_user.html', {'user' : user, 'loged_user' : loged_test })