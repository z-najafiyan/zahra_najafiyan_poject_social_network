from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from apps.account.models import User


class SignUpUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'user_name')
        # widgets = {
        #               'first_name': forms.TextInput(attrs={'class': 'input_class'}),
        #           }, {
        #               'last_name': forms.TextInput(attrs={'class': 'input_class'}),
        #           }, {
        #               'user_name': forms.TextInput(attrs={'class': 'input_class'}),
        #           }, {
        #               'password1': forms.PasswordInput(attrs={'class': 'input_class'}),
        #           }, {
        #               'password2': forms.PasswordInput(attrs={'class': 'input_class'}),
        #           }


class ActivateUserWithPhoneNumber(forms.ModelForm):
    cod = forms.CharField(max_length=4, label='Confirmation code')

    class Meta:
        model = User
        fields = ['cod']


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'password']
        widgets = {
            "password": PasswordInput(
                attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
        }

    def clean(self):
        # cleaned_data = super().clean()
        cleaned_data = self.cleaned_data
        user_name = cleaned_data.get("user_name")
        if not User.objects.filter(user_name=user_name).exists():
            raise ValidationError("No Email")
        else:
            return cleaned_data


class SearchUserForm(forms.ModelForm):
    search = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['search']
        widgets = {
            'placeholder': "Text to search"}


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'bio', 'photo_profile', 'gender', 'website')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
