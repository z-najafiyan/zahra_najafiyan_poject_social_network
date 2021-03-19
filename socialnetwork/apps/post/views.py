from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import UpdateView

from apps.account.models import User
from apps.post.forms import NewPostForm, CommentForm
from apps.post.models import Post, Comment


class NewPost(LoginRequiredMixin, View):
    """view form, new post
         input: attribute Post
         output: save post,
     """

    def get(self, request):
        form = NewPostForm()
        author = request.user
        return render(request, 'post/new_post_form.html', {'form': form, 'author': author})

    def post(self, request):
        form = NewPostForm(request.POST, request.FILES)
        author = request.user
        if form.is_valid():
            data = form.cleaned_data
            post = Post(title=data['title'], created_on=data['created_on'], content=data["content"],
                        author=User.objects.get(pk=author.id), updated_on=data['updated_on'], status=data['status'],
                        picture=data['picture'])
            post.save()

            return render(request, 'post/new_post_form.html',
                          {'form': form, 'author': author, 'message': "save  post"})
        return render(request, 'post/new_post_form.html',
                      {'form': form, 'author': author, 'message': "save not post"})


class DetailPostAuthor(LoginRequiredMixin, View):
    """
    View author post details and the lifespan of that post
    input: post title(slug)
    output: post details and lifespan of post

    """

    def get(self, request, other_user_pk, slug):
        post = Post.objects.filter(author_id=other_user_pk).filter(slug=slug).values('pk', 'title', 'created_on',
                                                                                     'content', 'author__email',
                                                                                     'picture', 'slug')
        time = post[0]['created_on']
        life_time = Post.objects.life_time(time=time)
        form = CommentForm()
        return render(request, "post/post_detail.html",
                      {'post': post[0], 'life_time': life_time, 'form': form})

    def post(self, request, other_user_pk, slug):
        """ comment form method post """
        detail_post = Post.objects.filter(author=other_user_pk).filter(slug=slug).values('pk', 'title', 'created_on',
                                                                                         'content', 'author__email',
                                                                                         'slug', 'picture')
        time = detail_post[0]['created_on']
        life_time = Post.objects.life_time(time=time)
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)
        # user_login = get_object_or_404(User, pk=request.user.id)

        if form.is_valid():
            data = form.cleaned_data
            # comment = Comment(user_id=user_login.id, post_id=post.pk, comment=data['comment'])
            comment = Post.comment.through.objects.create(user_id=request.user.id, post_id=post.pk,
                                                          comment=data['comment'])
            comment.save()
            return render(request, 'post/post_detail.html',
                          {'post': detail_post[0], 'life_time': life_time, 'form': form,
                           'message': "comment save"})
        return render(request, 'post/post_detail.html',
                      {'post': detail_post[0], 'life_time': life_time, 'form': form,
                       'message': "comment not save"})


class UpdatePost(UpdateView):
    model = Post
    template_name = 'post/edit_post.html'
    fields = ['title', 'content', 'updated_on', 'status', 'picture']
    success_url = 'profile'


class DeletePost(View):
    def get(self, request, slug):
        Post.objects.filter(slug=slug).delete()
        user = request.user.id
        return redirect('ok')
        # return reverse('profile',args=user)


class DeleteComment(View):
    def get(self, request, pk):
        user = request.user.id
        result = Comment.objects.delete_comment(comment_pk=pk, login_user_pk=user)
        if result:
            return redirect('ok')
        else:
            return redirect("404")
