import hashlib

from django.db import models

from common.validator import password_validator


class User(models.Model):
    username = models.EmailField("Email address", help_text="Enter an emil address")
    password = models.CharField(max_length=8, help_text="Enter an 8-character password",
                                validators=[password_validator])
    login = models.BooleanField(blank=True, null=True, default=False)
    photo_profile = models.ImageField('photo profile', upload_to='profile/%y/%m/%d/', blank=True, null=True)
    follow = models.ManyToManyField('account.User', related_name='following', through='Follow')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
        super().save(*args, **kwargs)
