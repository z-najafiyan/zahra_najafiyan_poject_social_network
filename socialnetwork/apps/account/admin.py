# Register your models here.
from django.contrib import admin

from apps.account.models.follow import Follow
from apps.account.models.user import User


# class FollowInline(admin.TabularInline):
#     model = Follow
#     extra = 2
#
@admin.register((Follow))
class Followuser(admin.ModelAdmin):
    list_display = ['user','following']
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', "username"]
    list_display_links = ['id']
    fields = ['username', 'password', 'photo_profile', ]
    # readonly_fields = ['choose follow ']
    # inlines = (FollowInline,)
