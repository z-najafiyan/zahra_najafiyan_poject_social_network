import hashlib

from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField( unique=True,help_text="Enter an emil address")
    password = models.TextField(max_length=8, help_text="Enter an 8-character password")
    login = models.BooleanField(blank=True, null=True, default=False)
    # photo_profile = models.ImageField(upload_to='image', blank=True, null=True)
    picture = models.ImageField(upload_to='profile/user_{}/%y/%m/%d/'.format(id), blank=True, null=True)


    def str(self):
        return self.email

    def save(self, *args, **kwargs):
        print("save",self.password)
        self.password = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
        print("save",self.password)
        super().save(*args, **kwargs)
