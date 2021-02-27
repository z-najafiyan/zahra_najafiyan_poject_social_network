# Create your views here.
import hashlib

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from apps.user.forms import RegisterUserForms, LoginUserForms
from apps.user.models import User


class Register(View):
    def get(self, request):
        form = RegisterUserForms()
        return render(request, 'user/register_Form.html', {'form': form})

    def post(self, request):
        form = RegisterUserForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] == data['repeat_password']:
                # form.save()
                user_obj = User(email=data['email'], password=data['password'])
                print(user_obj)
                user_obj.save()
                return render(request, 'user/register_Form.html',
                              {'form': form, 'message': 'Registration done. Welcome to the website'})
            else:
                return render(request, 'user/register_Form.html',
                              {'form': form, 'message': 'Password and password repetition are not the same'})

        return render(request, 'user/register_Form.html',
                      {'form': form, 'message': 'Registration done. Welcome to the website'})


class Login(View):
    def get(self, request):
        form = LoginUserForms()
        return render(request, 'user/Login.html', {'form': form})

    def post(self, request):
        form = LoginUserForms(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            if not User.objects.all().filter(email=data['email']):
                # Check email address
                return render(request, 'user/Login.html', {'form': form, "message": 'No email'})
            else:
                # Check password
                if User.objects.get(email=data['email']).password == hashlib.sha256(
                        data['password'].encode("utf-8")).hexdigest():
                    user = User.objects.get(email=data['email'])
                    user.login = True
                    return render(request, 'user/successful_login.html', {'form': form, 'user': user})
                    # return redirect('user/profile.html')

                else:
                    return render(request, 'user/Login.html', {'form': form, 'message': "The password is incorrect"})

# class Search(View):
#     def get(self, request):
#         form = LoginUserForms()
#         return render(request, 'user/Login.html', {'form': form})
#
#     def post(self, request):
#         form = LoginUserForms(request.POST, request.FILES)
#         if form.is_valid():
#             data = form.cleaned_data
