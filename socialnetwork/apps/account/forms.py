import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from apps.account.models import User


class SingUpUserForm(UserCreationForm):
    # mobile_or_email = forms.CharField(max_length=50, label="Enter email or phone number")

    class Meta:
        model = User
        fields = ['first_name', 'last_name','user_name','email']
# class SingUpUserForm(UserCreationForm):
#     # mobile_or_email = forms.CharField(max_length=50, label="Enter email or phone number")
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'user_name']

    # def clean_mobile_or_email(self):
    #     mobile_or_email =self.cleaned_data['mobile_or_email']
    #     regex = "(\+98|0)?9\d{9}"
    #     phone_number_match = re.match(regex, mobile_or_email)
    #     if not phone_number_match:
    #         if mobile_or_email.find("@") != -1:
    #             print("eeemail")
    #             try:
    #                 print("ffd")
    #                 validate_email(mobile_or_email)
    #             except validate_email.ValidationError:
    #                 print("ffss")
    #                 raise ValidationError('Invalid Email')
    #         else:
    #             raise ValidationError('Invalid phone number')
    #     print(mobile_or_email)
    #     return mobile_or_email


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'password']


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
        fields = ('first_name', 'last_name', 'gender', 'bio', 'photo_profile', 'gender', 'website')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
