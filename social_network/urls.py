from django.urls import path
from social_network.views import (
    PostCreateView,
    PostLikeView,
    PostUnlikeView,
    AnalyticsView,
    UserActivityView,
    UserSignupView,
    UserLoginView
)

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user-signup"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/like/", PostLikeView.as_view(), name="post-like"),
    path("post/<int:pk>/unlike/", PostUnlikeView.as_view(), name="post-unlike"),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
    path("user-activity/", UserActivityView.as_view(), name="user-activity"),
]
