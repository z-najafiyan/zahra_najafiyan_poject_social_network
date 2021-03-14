from django.db import models

from apps.account.managers import  RequestManagers


class RequestFollow(models.Model):
    request_user = models.ForeignKey('account.User', related_name='request_user', on_delete=models.CASCADE)
    request_follow = models.ForeignKey('account.User', related_name='request_followers', on_delete=models.CASCADE,
                                       blank=True,
                                       null=True)
    objects=RequestManagers()

    def __str__(self):
        return str(self.request_user.email)
