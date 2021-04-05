from django.db import models

from apps.account.maneger import FollowManege


class Follow(models.Model):
    user = models.ForeignKey('account.User', related_name='user', on_delete=models.CASCADE)
    following = models.ForeignKey('account.User', related_name='user_following', on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)
    objects = FollowManege()

    def __str__(self):
        return 'user:{},following:{}'.format(str(self.user),str(self.following))
