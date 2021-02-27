from django.urls import path

from apps.post.views import ListPostAuthor
from apps.user.views import Login, Register

urlpatterns = [
    path('login/', Login.as_view(), name='user_login'),
    path('register/', Register.as_view(), name='user_register'),
    path('profile/',ListPostAuthor.as_view(),name='profile'),

]
