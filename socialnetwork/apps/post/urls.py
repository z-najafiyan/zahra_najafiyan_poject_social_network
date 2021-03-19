from django.urls import path

from apps.account.views import CompleteProfile
from apps.post.views import NewPost, DetailPostAuthor, UpdatePost, DeletePost, DeleteComment

urlpatterns = [
    path('new_post/', NewPost.as_view(), name='new_post'),
    path('detail_post/<int:other_user_pk>/<slug:slug>/', DetailPostAuthor.as_view(), name='detail_post'),
    path('edit_post/<slug:slug>/', UpdatePost.as_view(), name='edit_post'),
    path('delete_post/<slug:slug>/', DeletePost.as_view(), name='delete_post'),
    path("delete_comment/<int:pk>/",DeleteComment.as_view(),name="delete_comment")

]
