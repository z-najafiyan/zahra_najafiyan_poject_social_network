from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', "email"]
    list_display_links = ['id']
    fields = ['email', 'password', 'picture']