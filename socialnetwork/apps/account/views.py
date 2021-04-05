# Create your views here.
import hashlib

from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from apps.account.forms import RegisterUserForms, LoginUserForms, SearchUserForms
from apps.account.models import User, Follow


class Register(View):
    """view form, user register
        input: email, password, repeat password,photo
        output: save user,
    """

    def get(self, request):
        form = RegisterUserForms()
        return render(request, 'user/register_Form.html', {'form': form})

    def post(self, request):
        form = RegisterUserForms(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] == data['repeat_password']:
                # form.save()
                user_obj = User(username=data['username'], password=data['password'])

                user_obj.save()
                return render(request, 'user/register_Form.html',
                              {'form': form, 'message': 'Registration done. Welcome to the website'})
            else:
                return render(request, 'user/register_Form.html',
                              {'form': form, 'message': 'Password and password repetition are not the same'})

        return render(request, 'user/Login.html',
                      {'form': form, 'message': 'Enter again information'})


class Login(View):
    """view form, user login
        input: email, password,
        output: save user,
    """

    def get(self, request):
        form = LoginUserForms(request.POST)
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        form = LoginUserForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if not User.objects.all().filter(username=data['username']):
                # Check username address
                return render(request, 'index.html', {'form': form, "message": 'No email'})
            else:
                # Check password
                if User.objects.get(username=data['username']).password == hashlib.sha256(
                        data['password'].encode("utf-8")).hexdigest():
                    user = User.objects.filter(username=data['username']).values('pk')
                    pk = user[0]['pk']
                    x = User.objects.filter(pk=pk).update(login=True)
                    user = User.objects.filter(pk=pk).values('pk', 'username', 'login')
                    return render(request, 'index.html', {'user': user[0], "pk_login": pk})
                else:
                    return render(request, 'index.html', {'form': form, 'message': "The password is incorrect"})
        else:
            return render(request, 'index.html', {'form': form})


class UserListSearch(View):
    """
    user search
    input: One or more characters
    output :A list of emails that contain those search characters
    """

    def get(self, request, pk_login):
        form = SearchUserForms()
        return render(request, 'user/search.html', {'form': form, 'pk_login': pk_login})

    def post(self, request, pk_login):
        form = SearchUserForms(request.POST)

        if form.is_valid():
            data = User.objects.filter(username__icontains=form.cleaned_data['search'])
            return render(request, 'user/search.html', {'data': data, 'form': form, 'pk_login': pk_login})
        return render(request, 'user/search.html', {'form': form, 'pk_login': pk_login})


class UserList(ListView):
    model = User
    template_name = 'user/search.html'


class FollowingList(View):
    """show following list
    input: Id user
    output : following user name list
    """

    def get(self, request,pk):
        following = Follow.objects.following(pk)
        return render(request, "follow/following_list.html", {'following': following})


class FollowersList(View):
    """show followers list
    input: Id user
    output : followers user name list
    """

    def get(self, request, pk):
        followers = Follow.objects.followers(pk)
        return render(request, "follow/followers_list.html", {'followers': followers})
