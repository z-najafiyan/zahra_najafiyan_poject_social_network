from django import template

from apps.account.models import User
from apps.post.models import Post, Comment

register = template.Library()


@register.simple_tag()
def like_post(login_user_pk,slug_post):
    """
    like post
    input: slug post, id user

    """
    post = Post.objects.get(slug=slug_post)
    user = User.objects.get(pk=login_user_pk)
    like_user = Post.objects.filter(slug=slug_post).filter(like__email=user.email)
    if not like_user.exists():
        post.like.add(user)
        return "Post liked"


@register.simple_tag()
def count_like(pk):
    """
     Counting post like
     input: id post
     output: number of like post
    """
    return Post.like.through.objects.filter(post_id=pk).count()

@register.inclusion_tag('comment/comment_detail.html')
def comment_detail(slug):
    """
    show comment
    input:slug post
    output: author comment,text comment
    """
    comment = Comment.objects.filter(post__slug=slug)
    return {"comment": comment}
