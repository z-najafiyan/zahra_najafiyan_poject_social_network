from django import forms
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from apps.account.models import User, Follow


class RegisterUserForms(forms.ModelForm):
    repeat_password = forms.CharField(max_length=8)

    class Meta:
        model = User
        fields = ['username', 'password', 'repeat_password', 'photo_profile']
        widgets = {
            "password": PasswordInput(
                attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
        }

    def clean_username(self):
        email = self.cleaned_data['username']
        if User.objects.filter(username=email).exists():
            raise ValidationError("Email already exists")
        return email


class LoginUserForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            "password": PasswordInput(
                attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
        }


class SearchUserForms(forms.ModelForm):
    search = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['search']
        widgets = {
            'placeholder': "Text to search"}

