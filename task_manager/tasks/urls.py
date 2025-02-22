from django.urls import path
from .views import login_view, register_view, logout_view, dashboard_view, profile_view
from .views import task_list, add_task, edit_task, delete_task, mark_complete



urlpatterns = [
    path('', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('tasks/', task_list, name="task_list"),
    path('tasks/add/', add_task, name="add_task"),
    path('tasks/edit/<int:task_id>/', edit_task, name="edit_task"),
    path('tasks/delete/<int:task_id>/', delete_task, name="delete_task"),
    path('tasks/complete/<int:task_id>/', mark_complete, name="mark_complete"),
     path('profile/', profile_view, name="profile"),
]