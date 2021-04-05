from django.shortcuts import render, get_object_or_404
from django.views import View

from apps.account.models.user import User
from apps.post.forms import NewPostForm, CommentForm
from apps.post.models import Post, Comment


class NewPost(View):
    """view form, new post
         input: attribute Post
         output: save post,
     """

    def get(self, request, pk):
        form = NewPostForm()
        author = User.objects.filter(pk=pk).values('pk', 'username')

        return render(request, 'post/new_post_form.html', {'form': form, 'author': author[0]['username']})

    def post(self, request, pk):
        form = NewPostForm(request.POST, request.FILES)
        author = User.objects.filter(pk=pk).values('pk', 'username')
        if form.is_valid():
            data = form.cleaned_data
            post = Post(title=data['title'], created_on=data['created_on'], content=data["content"],
                        author=User.objects.get(pk=pk), updated_on=data['updated_on'], status=data['status'],
                        picture=['picture'])
            post.save()
            return render(request, 'post/new_post_form.html',
                          {'form': form, 'author': author[0]['username'], 'message': "save  post"})
        return render(request, 'post/new_post_form.html',
                      {'form': form, 'author': author[0]['username'], 'message': "save not post"})


class ListPostAuthor(View):
    """
    view a List of posts by an author
    input: Author id
    output:List of posts by an author
    """

    def get(self, request, pk_login, pk):
        posts = Post.objects.filter(author__in=[pk]).values("title", 'slug')
        count = Post.objects.filter(author__in=[pk]).count()
        comment = Comment.objects.filter(post=pk).values('user__username', 'comment')
        author = Post.objects.filter(author__in=[pk]).values('pk', 'author', 'author__username',
                                                             'author__photo_profile')
        if not posts:
            return render(request, 'post/profile.html', {"message": 'User has no posts'})

        return render(request, "post/profile.html",
                      {'posts': posts, 'author': author[0], 'cont': count, "pk_login": pk_login, 'comment': comment})


class DetailPostAuthor(View):
    """
    View author post details and the lifespan of that post
    input: post title(slug)
    output: post details and lifespan of post

    """

    def get(self, request, pk_login, slug):
        post = Post.objects.filter(slug=slug).values('pk', 'title', 'created_on', 'content', 'author__username',
                                                     'picture', 'slug')
        time = post[0]['created_on']
        life_time = Post.objects.life_time(time=time)
        form = CommentForm()
        return render(request, "post/post_detail.html",
                      {"pk_login": pk_login, 'post': post[0], 'life_time': life_time, 'form': form})

    def post(self, request, pk_login, slug):
        """ comment form method post """
        detail_post = Post.objects.filter(slug=slug).values('pk', 'title', 'created_on', 'content', 'author__username',
                                                            'slug','picture')
        time = detail_post[0]['created_on']
        life_time = Post.objects.life_time(time=time)
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)
        user_login = get_object_or_404(User, pk=pk_login)

        if form.is_valid():
            data = form.cleaned_data
            # comment = Comment(user_id=user_login.id, post_id=post.pk, comment=data['comment'])
            comment = Post.comment.through.objects.create(user_id=user_login.id, post_id=post.pk,
                                                          comment=data['comment'])
            comment.save()
            return render(request,'post/post_detail.html',
                          {"pk_login": pk_login, 'post': detail_post[0], 'life_time': life_time, 'form': form,
                           'message': "comment save"})
        return render(request,'post/post_detail.html',
                      {"pk_login": pk_login, 'post': detail_post[0], 'life_time': life_time, 'form': form,
                       'message': "comment not save"})
