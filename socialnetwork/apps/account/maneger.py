from django.db import models


class FollowManege(models.Manager):
    def following(self, pk):
        from apps.account.models.follow import Follow

        following = [i['following__username'] for i in
                     Follow.objects.filter(user=pk).values('following__username').distinct()]
        print(following)
        return following

    def followers(self, pk):
        from apps.account.models.follow import Follow
        followers = [i['user__username'] for i in Follow.objects.filter(following__in=[pk]).values('user__username')]
        print(followers)
        return followers
