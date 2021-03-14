from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.account.managers import UserManagers


class User(AbstractBaseUser, PermissionsMixin):
    CHOICE_GENDER = [('0', 'Prefer Not To Say'), ('1', "Female"), ('2', 'Male')]

    first_name = models.CharField('First Name', blank=True, null=True, max_length=30)
    last_name = models.CharField('Last Name', blank=True, null=True, max_length=30)
    email = models.EmailField('Address Email', unique=True)
    photo_profile = models.ImageField('Photo Profile', upload_to='profile/%y/%m/%d/', blank=True, null=True)
    gender = models.CharField("Gender", blank=True, null=True, max_length=1, choices=CHOICE_GENDER, default='0')
    bio = models.TextField("Bio", blank=True, null=True)
    website = models.URLField('Address Website', blank=True, null=True)
    follow = models.ManyToManyField('account.User', related_name='following',
                                    through='Follow')
    request_follow = models.ManyToManyField('account.User', related_name='RequestFollow',
                                            through='RequestFollow')
    is_active = models.BooleanField(_('active'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    objects = UserManagers()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        app_label = 'account'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return str(self.email)
