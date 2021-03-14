from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.account.models import User


class UserCreateForms(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', "email"]


class SearchUserForms(forms.ModelForm):
    search = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['search']
        widgets = {
            'placeholder': "Text to search"}


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'bio', 'photo_profile', 'gender', 'website')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
