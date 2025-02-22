from django import forms
from django.contrib.auth.models import User
from .models import Task, Profile

# Task Form
class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Deadline"
    )

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "deadline"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter task title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Task details", "rows": 3}),
            "priority": forms.Select(attrs={"class": "form-select"}),
        }

# User Update Form
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email"})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

# Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Tell us about yourself", "rows": 3})
    )

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']
