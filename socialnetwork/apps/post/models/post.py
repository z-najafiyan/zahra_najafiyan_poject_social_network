from django.db import models

# Create your models here.
from django.db import models
from django_extensions.db.fields import AutoSlugField

from apps.post.manege import PostManege
from apps.user.models import User


class Post(models.Model):
    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from=['title'],unique=True)
    created_on = models.DateTimeField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    picture = models.ImageField(upload_to='post/user_{}/%y/%m/%d/'.format(author), blank=True, null=True)

    objects=PostManege()
    def __str__(self):
        return self.title
