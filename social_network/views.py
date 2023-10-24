from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from social_network.models import Post, UserActivity
from social_network.serializers import (
    PostSerializer,
    UserActivitySerializer,
    UserSerializer,
    CustomPostSerializer,
    AnalyticsSerializer
)
from django.contrib.auth.models import User
from django.db.models import Count, F
from django.utils import timezone


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Both username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        user.last_login = timezone.now()
        user.save()
        return Response(
            {
                "access_token": access_token
             },
            status=status.HTTP_200_OK
        )


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.get_object().likes.filter(id=self.request.user.id).exists():
            return CustomPostSerializer
        return PostSerializer

    def perform_update(self, serializer):
        post = self.get_object()
        user = self.request.user

        if not post.likes.filter(id=user.id).exists():
            post.likes.add(user)
            post.save()


class PostUnlikeView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        post = self.get_object()
        user = self.request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            post.save()


class AnalyticsView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        analytics = Post.objects.filter(
            created_at__gte=date_from,
            created_at__lte=date_to
        ).annotate(like_count=Count("likes"))

        serializer = AnalyticsSerializer(analytics, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserActivityView(generics.RetrieveAPIView):
    serializer_class = UserActivitySerializer

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        user_activity, _ = UserActivity.objects.get_or_create(user_id=user_id)
        user_activity.last_login = User.objects.get(id=user_id).last_login
        user_activity.last_request = User.objects.get(id=user_id).useractivity.last_request
        if self.request.user.id == user_id:
            user_activity.last_request = timezone.now()
            user_activity.save()

        return user_activity
