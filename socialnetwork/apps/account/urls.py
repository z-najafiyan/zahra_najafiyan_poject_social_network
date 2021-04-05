from django.urls import path

from apps.account.views import Register, UserListSearch, FollowersList, FollowingList

urlpatterns = [
    path('register/', Register.as_view(), name='user_register'),
    path('search/<int:pk_login>/', UserListSearch.as_view(), name='search_result'),
    path('followers_list/<int:pk>/',FollowersList.as_view(),name='followers_list'),
    path('following_list/<int:pk>/',FollowingList.as_view(),name='following_list'),
]
