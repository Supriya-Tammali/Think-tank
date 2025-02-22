from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from datetime import date, timedelta
import plotly.graph_objects as go



@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(user=request.user)
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()
    total_tasks = tasks.count()
    today = date.today()
    
    # Task Completion Progress
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Notifications for upcoming tasks
    upcoming_tasks = tasks.filter(deadline__gte=today, deadline__lte=today + timedelta(days=2), completed=False)
    overdue_tasks = tasks.filter(deadline__lt=today, completed=False)

    # Task Trends Chart (Bar Graph)
    weekly_task_counts = [tasks.filter(deadline=today - timedelta(days=i)).count() for i in range(7)]
    bar_chart = go.Figure([go.Bar(x=["Today", "1d Ago", "2d Ago", "3d Ago", "4d Ago", "5d Ago", "6d Ago"], y=weekly_task_counts)])
    bar_chart.update_layout(title_text="Tasks Completed in the Last 7 Days", xaxis_title="Days", yaxis_title="Tasks")
    bar_chart_html = bar_chart.to_html(full_html=False)

    # Task Completion Pie Chart
    pie_chart = go.Figure(data=[go.Pie(labels=["Completed", "Pending"], values=[completed_tasks, pending_tasks], hole=0.4)])
    pie_chart.update_layout(title_text="Task Completion Status")
    pie_chart_html = pie_chart.to_html(full_html=False)

    return render(request, "dashboard.html", {
        "tasks": tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_percentage": completion_percentage,
        "upcoming_tasks": upcoming_tasks,
        "overdue_tasks": overdue_tasks,
        "pie_chart_html": pie_chart_html,
        "bar_chart_html": bar_chart_html,
    })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard") 
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "auth/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form, "action": "Add Task"})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "action": "Edit Task"})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("task_list")

@login_required
def mark_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect("task_list")

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("dashboard")  

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "profile.html", {"user_form": user_form, "profile_form": profile_form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    today = date.today()
    upcoming_tasks = tasks.filter(deadline__gte=today, deadline__lte=today + timedelta(days=2), completed=False)
    overdue_tasks = tasks.filter(deadline__lt=today, completed=False)

    # Notify user about overdue tasks
    if overdue_tasks.exists():
        messages.error(request, "⚠️ You have overdue tasks! Please complete them ASAP.")

    # Notify user about upcoming tasks
    if upcoming_tasks.exists():
        messages.warning(request, "⏳ You have tasks due soon. Don't forget to complete them!")

    return render(request, "tasks/task_list.html", {"tasks": tasks})   