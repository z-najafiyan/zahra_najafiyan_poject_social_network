from random import randint

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView

from apps.account.forms import SearchUserForm, UserUpdateForm, LoginUserForm, \
    SingUpUserForm
from apps.account.models import User, Follow, RequestFollow
from apps.account.tokens import account_activation_token
from apps.post.models import Post, Comment
from kavenegar import *

from common.sms import kave_negar_token_send
from socialnetwork.settings import API_KEY


class SingUp(View):
    """view form, user register
        input: email, password, repeat password,photo
        output: save Account,
    """

    def get(self, request):
        form = SingUpUserForm()
        return render(request, 'sing_up.html', {'form': form})

    def post(self, request):
        form = SingUpUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['mobile_or_email'].find('@') != -1:
                user = User(first_name=data['first_name'], last_name=data['last_name'],
                            user_name=data['mobile_or_email'],
                            phone_number=data['mobile_or_email'], is_active=False)
                user.save()
                token = randint(1000, 9999)
                user.token_sms = token
                user.save()
                kave_negar_token_send(data['phone_number'], token)
                return render(request, 'user/activation_sms.html', {'id_user': user.id})

            else:
                user = User(first_name=data['first_name'], last_name=data['last_name'],
                            user_name=data['mobile_or_email'],
                            email=data['mobile_or_email'], is_active=False)

                # user.save(commit=False)
                # user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('user/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = SingUpUserForm()
        return render(request, 'sing_up.html', {'form': form})


class CheckActivationCode(View):
    def get(self, request, id):
        code = request.GET.get('activation_code')
        user = User.objects.get(pk=id)
        if user.token_sms == code:
            user.is_active = True
            user.save()
            return reverse("login")
        else:
            token = randint(1000, 9999)
            user.token_sms = token
            user.save()
            kave_negar_token_send(user.phone_number, token)
            return render(request, 'user/activation_sms.html', {'id_user': user.id})


class ActivateView(View):
    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


class LoginView(View):
    def get(self, request):
        form = LoginUserForm()
        next = request.GET.get('next')
        return render(request, 'login.html', {'next': next})

    @csrf_exempt
    def post(self, request):
        form = LoginUserForm(request.POST)
        message = ''
        is_logout = request.POST.get("logout")
        next = request.GET.get('next')

        if form.is_valid():
            data = form.cleaned_data
            if not User.objects.all().filter(username=data['username']):
                # Check username address
                return render(request, 'index.html', {'form': form, "message": 'No email'})
            else:
                # Check password
                user = authenticate(username=data['user_name'], password=data["password"])
                if user is not None:
                    if user.is_active:
                        message = 'Login was successful!'
                        login(request, user)
                        if next:
                            return redirect(next)
                else:
                    message = 'Username or password was wrong!'
        elif is_logout:
            logout(request)
            message = 'Logout successful'
        return render(request, 'login.html', {'message': message, 'next': next})


def logout_view(request):
    logout(request)


class UserListSearch(LoginRequiredMixin, View):
    """
    user search
    input: One or more characters
    output :A list of emails that contain those search characters
    """

    def get(self, request):
        form = SearchUserForm()
        return render(request, 'user/search.html', {'form': form})

    def post(self, request):
        form = SearchUserForm(request.POST)
        if form.is_valid():
            data = User.objects.filter(email__icontains=form.cleaned_data['search'])
            return render(request, 'user/search.html', {'data': data, 'form': form})
        return render(request, 'user/search.html', {'form': form})


class UserList(ListView):
    model = User
    template_name = 'user/search.html'


class FollowingList(LoginRequiredMixin, View):
    """show following list
    input: Id user
    output : following user name list
    """

    def get(self, request, other_user_pk):
        following = Follow.objects.following(other_user_pk)
        return render(request, "follow/following_list.html", {'following': following})


class FollowersList(LoginRequiredMixin, View):
    """show followers list
    input: Id user
    output : followers user name list
    """

    def get(self, request, other_user_pk):
        followers = Follow.objects.followers(other_user_pk)
        return render(request, "follow/followers_list.html", {'followers': followers})


class ProfileUser(View):
    """
    view a List of posts by an author
    input: Author id
    output:List of posts by an author
    """

    def get(self, request, other_user_pk):
        posts = Post.objects.filter(author__in=[other_user_pk]).values("title", 'slug')
        count = Post.objects.filter(author__in=[other_user_pk]).count()
        comment = Comment.objects.filter(post=other_user_pk).values('user__first_name', 'user__last_name', 'comment')
        author = Post.objects.filter(author__in=[other_user_pk]).values('pk', 'author', 'author__first_name',
                                                                        'author__last_name')
        profile = User.objects.filter(pk=other_user_pk).values('id', 'bio', 'first_name', 'last_name', 'photo_profile',
                                                               'website')

        if not posts:
            return render(request, 'user/profile_without_post.html',
                          {"message": 'User has no posts', 'profile': profile[0]})
        return render(request, "user/profile.html",
                      {'posts': posts, 'author': author[0], 'count': count, 'comment': comment, 'profile': profile[0]})


class CompleteProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'registration/edit_user.html'
    # success_url = 'profile/'


class ListRequest(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        request_follow = RequestFollow.objects.filter(request_user=user.id).values("request_follow__email",
                                                                                   "request_follow")
        return render(request, "request/request_follow_list.html", {"request_follow": request_follow})


class AcceptRequest(View):
    def get(self, request, other_user_pk):
        login_user_pk = request.user.id
        RequestFollow.objects.accept_request(login_user_pk, other_user_pk)
        request_follow = RequestFollow.objects.filter(request_user=login_user_pk).values("request_follow__email",
                                                                                         "request_follow")
        return render(request, "request/request_follow_list.html", {"request_follow": request_follow})


class DeleteRequest(View):
    def get(self, request, other_user_pk):
        login_user_pk = request.user.id
        RequestFollow.objects.delete_request(login_user_pk, other_user_pk)
        request_follow = RequestFollow.objects.filter(request_user=login_user_pk).values("request_follow__email",
                                                                                         "request_follow")
        return render(request, "request/request_follow_list.html", {"request_follow": request_follow})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })


class HomePage(View):
    def get(self, request):
        user = request.user.id
        following_user = Follow.objects.following(pk=user)
        posts = Post.objects.filter(author__in=following_user).order_by('created_on').values('title', "created_on",
                                                                                             "content",
                                                                                             "author__first_name",
                                                                                             'author__last_name',
                                                                                             'picture',
                                                                                             'life_time')
        return render(request, 'index.html', {'posts': posts})
