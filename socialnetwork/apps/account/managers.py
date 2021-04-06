from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Q


class UserManagers(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_name, password, **extra_fields):
        if not user_name:
            raise ValueError('The given email or phone number must be set')
        if user_name.find("@") != -1:
            user_name = self.normalize_email(user_name)
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(user_name, password, **extra_fields)

    def create_superuser(self, user_name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(user_name, password, **extra_fields)


class FollowManagers(models.Manager):
    def following(self, pk):
        following = [i['following__first_name'] + " " + i['following__last_name'] for i in
                     self.filter(user=pk).values('following__last_name', 'following__first_name').distinct()]
        return following

    def followers(self, pk):
        followers = [i['user__first_name'] + " " + i['user__last_name'] for i in
                     self.filter(following__in=[pk]).values('user__first_name', 'user__last_name')]
        return followers


class RequestManagers(models.Manager):
    def request_following_user(self, pk_user_login, pk_other_user):
        """
        Follow the user
        :param  pk_user_login:
        :param pk_other_user:
        :return: message
        """
        from apps.account.models import Follow
        from apps.account.models import User
        login_user = User.objects.get(pk=pk_user_login)
        other_user = User.objects.get(pk=pk_other_user)

        request_repeated = self.filter(request_user=other_user.pk).filter(request_follow=pk_user_login).exists()
        following_repeated = Follow.objects.filter(user=pk_other_user).filter(following=pk_user_login).exists()
        if not following_repeated and not request_repeated:
            if pk_other_user == pk_user_login:
                message = "You can not follow yourself"
                return message
            else:
                request = self.create(request_user=other_user, request_follow=login_user)
                request.save()
                message = "{} followed {}".format(login_user, other_user)
                return message
        else:
            message = 'You have already requested or are following the user'
            return message

    def accept_request(self, pk_user_login, pk_other_user):
        from apps.account.models import User
        from apps.account.models import Follow
        login_user = User.objects.get(pk=pk_user_login)
        other_user = User.objects.get(pk=pk_other_user)
        request = self.filter(Q(request_user=pk_user_login) & Q(request_follow=pk_other_user))
        if request:
            self.filter(Q(request_user=pk_user_login) & Q(request_follow=pk_other_user)).delete()
            following = Follow.objects.create(user=login_user, following=other_user)
            following.save()
            return "user followers"

    def delete_request(self, pk_user_login, pk_other_user):
        request = self.filter(Q(request_user=pk_user_login) & Q(request_follow=pk_other_user)).exists()
        if not request:
            self.filter(Q(request_user=pk_user_login) & Q(request_follow=pk_other_user)).delete()
            return "request delete"
