from django import template

from apps.account.models import User, Follow
from apps.post.models import Post

register = template.Library()


@register.inclusion_tag('user/user_list.html')
def user_list(pk_login):
    """show user name list"""
    users = User.objects.all()
    return {"users": users, 'pk_login': pk_login}


@register.inclusion_tag('user/following_post_list.html')
def following_post_list(pk):
    """show user following
     input:pk user
     output: list following
     """
    following = Follow.objects.following(pk)
    posts = Post.objects.filter(author__username__in=following).values('title', 'author__username')
    return {'posts': posts, 'pk_login': pk}


@register.simple_tag()
def follow_user(pk_login, pk_other):
    """
    Follow the user
    :param pk_login:
    :param pk_other:
    :return: message
    """
    login_user = User.objects.get(pk=pk_login)
    other_user = User.objects.get(pk=pk_other)
    if Follow.objects.filter(user=login_user.id).filter(following=other_user.pk).exists():
        f = Follow(user=login_user, following=other_user)
        f.save()
        message = "{} followed {}".format(login_user, other_user)
        return message

    elif pk_other == pk_login:
        message = "You can not follow yourself"
        return message
    else:
        message = 'You can only follow one user once'
        return message


@register.simple_tag()
def count_followers(pk):
    """ count followers user"""

    followers = Follow.objects.followers(pk)
    return len(followers)


@register.simple_tag()
def count_following(pk):
    """ count following user"""
    following = Follow.objects.following(pk)
    return len(following)
