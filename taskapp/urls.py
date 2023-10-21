from django.urls import path, include
from taskapp.views import completed_task, home, pending_task, edit_own_profile, download_excel, add_task, edit_user, edit_task, main, update_task ,signup, signin, logout_view, add_client, get_task_details, get_client_data
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
    path('get_task_details/<int:task_id>/', get_task_details, name='get_task_details'),
    path('update_task/<int:task_id>/', update_task, name='update_task'),
    path('get_client_data/<int:client_id>/', get_client_data, name='get_client_data'),
    path('download-excel/', download_excel, name='download_excel'),
    path('edit_profile/', edit_own_profile, name='edit_own_profile'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('edit-task/', edit_task, name='edit_task')


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)