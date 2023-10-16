from django.urls import path, include
from taskapp.views import completed_task, home, pending_task, add_task, edit_task, main, signup, signin, logout_view, add_client
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', signin, name="signin"),
    path('', home, name="home"),
    path('completed-task/', completed_task, name="completed_task"),
    path('pending-task/', pending_task, name="pending_task"),
    path('add-task/', add_task, name="add_task"),
    path('add_client/', add_client, name="add_client"),
    path('main/', main, name="main"),
    path('signup/', signup, name="signup"),
    path('logout/', logout_view, name="logout"),
    path('edit-task/<int:task_id>/', edit_task, name='edit_task')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)