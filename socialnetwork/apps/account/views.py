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
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView

from socialnetwork.apps.account.forms import SearchUserForm, UserUpdateForm, LoginUserForm, \
    SignUpUserForm, ActivateUserWithPhoneNumber
from socialnetwork.apps.account.models import User, Follow, RequestFollow
from socialnetwork.apps.account.tokens import account_activation_token
from socialnetwork.apps.post.models import Post, Comment
from socialnetwork.common.sms import kave_negar_token_send


class SignUp(View):
    """view form, user register
        input: email, password, repeat password,photo
        output: save Account,
    """

    def get(self, request):
        form = SignUpUserForm()
        return render(request, 'sign_up.html', {'form': form})

    def post(self, request):
        form = SignUpUserForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if data['user_name'].find('@') == -1:
                user = form.save(commit=False)
                user.is_active = False
                user.phone_number = data['user_name']
                user.save()
                token = randint(1000, 9999)
                user.token_sms = token
                user.save()
                kave_negar_token_send(data['user_name'], token)
                return render(request, 'user/activation_sms.html', {'id_user': user.id})
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.email = data['user_name']
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('user/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('user_name')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            error = form.errors
            form = SignUpUserForm()
        return render(request, 'sign_up.html', {'form': form, 'error': error})


class CheckActivationCode(View):
    def get(self, request, pk):
        form = ActivateUserWithPhoneNumber()
        return render(request, 'user/activation_sms.html', {'form': form, 'pk': pk})

    def post(self, request, pk):
        form = ActivateUserWithPhoneNumber(request.POST)
        user = User.objects.get(pk=pk)
        if form.is_valid():
            if user.token_sms == form.cleaned_data['cod']:
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
            return reverse("login")
        else:
            return HttpResponse('Activation link is invalid!')


class SignIn(View):
    def get(self, request):
        form = LoginUserForm()
        next = request.GET.get('next')
        return render(request, 'sign_in.html', {'next': next, 'form': form})

    @csrf_exempt
    def post(self, request):
        form = LoginUserForm(request.POST)
        message = ''
        is_logout = request.POST.get("logout")
        next = request.GET.get('next')

        if form.is_valid():
            data = form.cleaned_data
            if not User.objects.all().filter(user_name=data['user_name']):
                # Check username address
                return render(request, 'index.html', {'form': form, "message": 'No email'})
            else:
                # Check password
                user = authenticate(user_name=data['user_name'], password=data["password"])
                if user is not None:
                    if user.is_active:
                        message = 'Login was succesasful!'
                        login(request, user)
                        if next:
                            return redirect(next)
                        else:
                            return redirect('home')

                else:
                    message = 'Username or password was wrong!'
        elif is_logout:
            logout(request)
            message = 'Logout successful'
        return render(request, 'sign_in.html', {'form': form, 'message': message, 'next': next})


def logout_view(request):
    logout(request)
    return redirect('home')


class UserListSearch(LoginRequiredMixin, View):
    """
    user search
    input: One or more characters
    output :A list of emails that contain those search characters
    """

    def get(self, request):
        form = SearchUserForm()
        data = " "
        return render(request, 'user/search.html', {'form': form, 'data': data})

    def post(self, request):
        form = SearchUserForm(request.POST)
        if form.is_valid():
            data = User.objects.filter(user_name__icontains=form.cleaned_data['search']).values('first_name',
                                                                                                'last_name', 'pk')
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
        return render(request, "follow/following_list.html", {'following': following, "other_user_pk": other_user_pk})


class FollowersList(LoginRequiredMixin, View):
    """show followers list
    input: Id user
    output : followers user name list
    """

    def get(self, request, other_user_pk):
        followers = Follow.objects.followers(other_user_pk)
        return render(request, "follow/followers_list.html", {'followers': followers, "other_user_pk": other_user_pk})


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


class EditCompleteUser(LoginRequiredMixin, UpdateView):
    """edit and complete profile """
    model = User
    form_class = UserUpdateForm
    template_name = 'registration/edit_user.html'

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"other_user_pk": self.request.user.pk})


class ListRequest(LoginRequiredMixin, View):
    """ Display user follow request """

    def get(self, request):
        user = request.user
        request_follow = RequestFollow.objects.filter(request_user=user.id).values("request_follow__first_name",
                                                                                   "request_follow__last_name",
                                                                                   "request_follow__photo_profile",
                                                                                   "request_follow")
        return render(request, "request/request_follow_list.html", {"request_follow": request_follow})


class AcceptRequest(View):
    """ Accept user follow request """

    def get(self, request, other_user_pk):
        login_user_pk = request.user.id
        RequestFollow.objects.accept_request(login_user_pk, other_user_pk)
        request_follow = RequestFollow.objects.filter(request_user=login_user_pk).values("request_follow__first_name",
                                                                                         "request_follow__last_name",
                                                                                         "request_follow__photo_profile",

                                                                                         "request_follow")

        return render(request, "request/request_follow_list.html", {"request_follow": request_follow})


class DeleteRequest(View):
    """ Delete user follow request """

    def get(self, request, other_user_pk):
        login_user_pk = request.user.id
        RequestFollow.objects.delete_request(login_user_pk, other_user_pk)
        request_follow = RequestFollow.objects.filter(request_user=login_user_pk).values("request_follow__first_name",
                                                                                         "request_follow__last_name",
                                                                                         "request_follow__photo_profile",
                                                                                         "request_follow")
        return render(request, "request/request_follow_list.html", {"request_follow": request_follow})


def change_password(request):
    """
    chage password
    :param request:
    :return:
    """
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


class HomePage(ListView):
    """
    Displays a list of posts the user is following
    """
    paginate_by = 4
    model = Post
    template_name = "index.html"

    def get_queryset(self):
        # qs= super().get_queryset()
        user = self.request.user.id
        following_user = [i['following'] for i in
                          Follow.objects.filter(user=user).values('following').distinct()]
        posts = Post.objects.filter(author__in=following_user).order_by('created_on')
        return posts


class SendRequestFollow(View):
    """
    Request to follow the user
    input : user (following)
    """

    def get(self, request, other_user_pk):
        pk_login_user = request.user.pk
        RequestFollow.objects.request_following_user(pk_login_user, other_user_pk)
        # return reverse("profile", args=int(other_user_pk))
        return redirect('profile', other_user_pk=other_user_pk)
