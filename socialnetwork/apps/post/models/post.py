# Create your models here.

from django.db import models
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField

from apps.post.managers import PostManege
from apps.post.models.comment import Comment



class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from=['title'], unique=True)
    created_on = models.DateTimeField(default=timezone.now())
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey('account.User', on_delete=models.DO_NOTHING)
    updated_on = models.DateTimeField(blank=True, null=True)
    picture = models.ImageField(upload_to='post/%y/%m/%d/', blank=True, null=True)
    like = models.ManyToManyField('account.User', related_name='like', null=True, blank=True)
    comment = models.ManyToManyField('account.User', related_name='comment', through=Comment)

    objects = PostManege()

    def __str__(self):
        return '{}'.format(self.title)

    @property
    def life_time(self):
        return Post.objects.life_time(self.created_on)
