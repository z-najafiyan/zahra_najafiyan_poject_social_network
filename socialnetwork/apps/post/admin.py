from apps.post.models import Post
from django.contrib import admin


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','author']
    list_display_links = ['id']
