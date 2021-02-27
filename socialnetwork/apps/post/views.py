from django.shortcuts import render

# Create your views here.
from django.utils.timezone import now
from django.views import View
from django.views.generic import DetailView

from apps.post.forms import NewPostForm
from apps.post.models import Post


class NewPost(View):
    def get(self, request):
        form = NewPostForm()
        return render(request, 'post/new_post_form.html', {'form': form})

    def post(self, request):
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'post/new_post_form.html', {'form': form, 'message': 'save post'})
        return render(request, 'post/new_post_form.html', {'form': form, 'message': "save not post"})


class ListPostAuthor(View):
    def get(self, request, pk):
        posts = Post.objects.filter(author=pk)
        count = posts.count()
        if not posts:
            return render(request, 'message.html', {"message": 'User has no posts'})
        return render(request, "post/profile.html", {'posts': posts, 'count': count})


#
# class DetailPostAuthor(DetailView):
#     model = Post
#
#     def get_context_data(self, **kwargs, ):
#         context = super().get_context_data(**kwargs)
#         print(kwargs)
#         context['object'] = Post.objects.all().filter().values('title', 'created_on', 'content', 'author')
#         time = context['object'][0]['created_on']
#         life_time = Post.objects.life_time(time=time)
#         context['life_time'] = life_time
#         return context
class DetailPostAuthor(View):
    def get(self, request, slug):
        post = Post.objects.filter(slug=slug).values('title', 'created_on', 'content', 'author')
        time = post[0]['created_on']
        life_time = Post.objects.life_time(time=time)
        post=post.values_list('title', 'created_on', 'content', 'author')
        return render(request, "post/post_detail.html", {'post': post, 'life_time': life_time})
