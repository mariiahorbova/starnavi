from django.urls import path
from social_network.views import (
    PostCreateView,
    PostLikeView,
    PostUnlikeView,
    AnalyticsView,
    UserActivityView,
    UserSignupView,
    UserLoginView,
    PostListView
)

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user-signup"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/like/", PostLikeView.as_view(), name="post-like"),
    path("posts/<int:pk>/unlike/", PostUnlikeView.as_view(), name="post-unlike"),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
    path("user-activity/<int:user_id>/", UserActivityView.as_view(), name="user-activity"),
]
