from django import template

from apps.account.models import User
from apps.post.models import Post, Comment

register = template.Library()


@register.simple_tag()
def like_post(slug_post, pk_user):
    """
    like post
    input: slug post, id user

    """
    post = Post.objects.get(slug=slug_post)
    user = User.objects.get(pk=pk_user)
    like_user = Post.objects.filter(slug=slug_post).filter(like__username=user.username)
    if not like_user.exists():
        # like = Post.like.through.objects.create(user_id=pk_user, post_id=post.pk)
        # like.save()
        post.like.add(user)
        return "Post liked"


@register.simple_tag()
def count_like(pk):
    """
     Counting post like
     input: id post
     output: number of like post
    """
    return Post.objects.filter(pk=pk).values('like').count()


@register.inclusion_tag('comment/comment_detail.html')
def comment_detail(slug):
    """
    show comment
    input:slug post
    output: author comment,text comment
    """
    comment = Comment.objects.filter(post__slug=slug)
    return {"comment": comment}
