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


class UserCreate(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=7, max_length=64)
    password2 = forms.CharField(widget=forms.PasswordInput(), min_length=7, max_length=64)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role', 'department', 'password', 'password2')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('رمز های عبور وارد شده بایکدیگر مغایرت دارند ')
        return p2


class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role', 'department', 'is_active')
