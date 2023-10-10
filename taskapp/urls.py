from django.urls import path, include
from taskapp.views import completed_task, home, pending_task, add_task, edit_task, main, signup, signin, logout_view

urlpatterns = [
    path('', signin, name="signin"),
    path('home', home, name="home"),
    path('completed-task/', completed_task, name="completed_task"),
    path('pending-task/', pending_task, name="pending_task"),
    path('add-task/', add_task, name="add_task"),
    path('main/', main, name="main"),
    path('signup/', signup, name="signup"),
    path('logout/', logout_view, name="logout"),
    path('edit-task/<int:task_id>/', edit_task, name='edit_task')

]