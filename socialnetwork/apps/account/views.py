from profile import Profile

from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

# Create your views here.
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from apps.account.forms import UserCreateForms, SearchUserForms, UserUpdateForm
from django.contrib import messages

from apps.account.models import User, Follow, RequestFollow
from apps.post.models import Post, Comment


class Register(CreateView):
    """view form, user register
        input: email, password, repeat password,photo
        output: save Account,
    """
    form_class = UserCreateForms
    success_url = '/login'
    template_name = 'registration/register_user.html'

    def post(self, request):
        messages.success(request, 'User was successfully created.')
        return super(Register, self).post(request)


def logout_view(request):
    logout(request)


class UserListSearch(LoginRequiredMixin, View):
    """
    user search
    input: One or more characters
    output :A list of emails that contain those search characters
    """

    def get(self, request):
        form = SearchUserForms()
        return render(request, 'user/search.html', {'form': form})

    def post(self, request):
        form = SearchUserForms(request.POST)
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
        request_follow = RequestFollow.objects.filter(request_user=user.id).values("request_follow__email","request_follow")
        return render(request, "request/request_follow_list.html", {"request_follow": request_follow})

class AcceptRequest(View):
    def get(self, request, other_user_pk):
        login_user_pk = request.user.id
        RequestFollow.objects.accept_request(login_user_pk, other_user_pk)
        request_follow = RequestFollow.objects.filter(request_user=login_user_pk).values("request_follow__email","request_follow")
        return render(request, "request/request_follow_list.html", {"request_follow": request_follow})


class DeleteRequest(View):
    def get(self, request, other_user_pk):
        login_user_pk = request.user.id
        RequestFollow.objects.delete_request(login_user_pk, other_user_pk)
        request_follow = RequestFollow.objects.filter(request_user=login_user_pk).values("request_follow__email","request_follow")
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