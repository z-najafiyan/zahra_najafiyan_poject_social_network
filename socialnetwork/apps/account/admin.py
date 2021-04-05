from django.contrib import admin

# sign up your models here.
from socialnetwork.apps.account.models import User, Follow


@admin.register(Follow)
class Followers(admin.ModelAdmin):
    list_display = ['user', 'following']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', "email"]
    list_display_links = ['id']
    # readonly_fields = ['choose follow ']
    # inlines = (FollowInline,)
