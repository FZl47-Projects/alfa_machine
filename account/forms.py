from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=7, max_length=64)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role', 'department', 'password')
