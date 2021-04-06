from django import template

from apps.account.models import User, Follow, RequestFollow
from apps.post.models import Post

register = template.Library()


@register.inclusion_tag('user/user_list.html')
def user_list():
    """show user name list"""
    users = User.objects.all()
    return {"users": users}


# @register.inclusion_tag('user/following_post_list.html')
# def following_post_list(pk):
#     """show user following
#      input:pk user
#      output: list following
#      """
#     following = Follow.objects.following(pk)
#     posts = Post.objects.filter(author__email__in=following).values('title', 'author__email')
#     return {'posts': posts}


# @register.simple_tag()
# def send_request_follow(pk_login_user, pk_other_user):
#     """
#     Follow the user
#     :param pk_login_user:
#     :param pk_other_user:
#     :return: message
#     """
#     return RequestFollow.objects.request_following_user(pk_login_user, pk_other_user)


@register.simple_tag()
def accept_request(pk_login_user, pk_other_user):
    RequestFollow.objects.accept_request(pk_login_user, pk_other_user)
    return "accept request"


@register.simple_tag()
def delete_request(pk_login_user, pk_other_user):
    RequestFollow.objects.delete_request(pk_login_user, pk_other_user)
    return "delete request"


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
