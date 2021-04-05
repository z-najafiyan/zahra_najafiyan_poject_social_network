from django.urls import path

from apps.post.views import NewPost, ListPostAuthor, DetailPostAuthor


urlpatterns = [
    path('new_post/<int:pk>/', NewPost.as_view(), name='nem_post'),
    path('show_posts/<int:pk_login>/profile/<int:pk>/', ListPostAuthor.as_view(), name='profile'),
    path('detail_post/<int:pk_login>/<slug:slug>/', DetailPostAuthor.as_view(), name='detail_post'),

]
