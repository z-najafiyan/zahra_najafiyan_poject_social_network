from django.contrib import admin

from apps.post.models.post import Post


@admin.register(Post)
class Post_admin(admin.ModelAdmin):
    fields = ['title', 'created_on', 'content', 'author', 'status']
    list_display = ['title', 'created_on', 'author', 'status']
    list_display_links = ['title']
