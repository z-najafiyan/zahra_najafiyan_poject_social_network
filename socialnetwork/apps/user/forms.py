import hashlib

from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput, EmailInput


class RegisterUserForms(forms.ModelForm):
    repeat_password = forms.CharField(max_length=8)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeat_password', ]
        widgets = {
            "password": PasswordInput(
                attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
            "repeat_password": PasswordInput(
                attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
        }

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     print("save", self.password)
    #     self.password = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
    #     print("save", self.password)



class LoginUserForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', ]
        widgets = {
            "password": PasswordInput(
                attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
        }
class SearchUserForms(forms.ModelForm):
    class Meta:
        model=User
        fields=['email']
        widgets={'email':EmailInput(attrs={'autocomplete':'on','data-r=toggle':'email'}),
                 }