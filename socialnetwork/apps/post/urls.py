from django.urls import path

from apps.post.views import NewPost, ListPostAuthor, DetailPostAuthor

urlpatterns = [
    path('new_post/', NewPost.as_view(), name='nem_post'),
    path('show_posts/<int:pk>/', ListPostAuthor.as_view(), name='profile'),
    path('detail_post/<slug:slug>/', DetailPostAuthor.as_view(), name='detail_post'),
]
