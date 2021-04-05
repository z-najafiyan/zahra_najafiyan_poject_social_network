from django.db import models


class Comment(models.Model):
    user = models.ForeignKey('account.User', blank=True, null=True, related_name='user_comment',
                             on_delete=models.CASCADE)
    post = models.ForeignKey('post.Post', blank=True, null=True, related_name='post_comment', on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return "user: {} ,post: {} ,comment:{}".format(self.user, self.post, self.comment)
