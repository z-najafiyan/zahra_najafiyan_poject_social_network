from django.urls import path

from apps.account.views import UserListSearch, FollowingList, FollowersList, ProfileUser, \
    ListRequest, AcceptRequest, DeleteRequest, SendRequestFollow

urlpatterns = [
    # path('register/', SignUp.as_view(), name='user_sign_up'),
    path('search/', UserListSearch.as_view(), name='search_result'),
    path('followers_list/<int:other_user_pk>/', FollowersList.as_view(), name='followers_list'),
    path('following_list/<int:other_user_pk>/', FollowingList.as_view(), name='following_list'),
    path('profile/<int:other_user_pk>/', ProfileUser.as_view(), name="profile"),
    path('requesst_list/', ListRequest.as_view(), name='request'),
    path('request_list/<int:other_user_pk>/', AcceptRequest.as_view(), name='accept_request'),
    path('request_list/<int:other_user_pk>/', DeleteRequest.as_view(), name='delete_request'),
    path("send_request_follow/<int:other_user_pk>/", SendRequestFollow.as_view(), name="send_request_follow"),
]
