# Create your models here.
from django.db import models
from django_extensions.db.fields import AutoSlugField

from apps.post.maneger import PostManege
from apps.post.models.comment import Comment


class Post(models.Model):
    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from=['title'], unique=True)
    created_on = models.DateTimeField()
    content = models.TextField()
    author = models.ForeignKey('account.User', on_delete=models.DO_NOTHING)
    updated_on = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    picture = models.ImageField(upload_to='post/%y/%m/%d/', blank=True, null=True)
    like = models.ManyToManyField('account.User', related_name='like', null=True, blank=True)
    comment = models.ManyToManyField('account.User', related_name='comment', through=Comment)

    objects = PostManege()

    def __str__(self):
        return '{} , {} ,{},{}'.format(self.id, self.title, self.author, self.like)

    @property
    def life_time(self):
        return Post.objects.life_time(self.created_on)
