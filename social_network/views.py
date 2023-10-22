from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from social_network.models import Post, UserActivity
from social_network.serializers import (
    PostSerializer,
    UserActivitySerializer,
    UserSerializer
)
from django.contrib.auth.models import User
from django.db.models import Count, F
from django.utils import timezone


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer

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

        return Response(
            {"access_token": access_token},
            status=status.HTTP_200_OK
        )


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(likes=F("likes") + 1)


class PostUnlikeView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(likes=F("likes") - 1)


class AnalyticsView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        analytics = Post.objects.filter(
            created_at__range=[date_from, date_to]).values(
            "created_at"
        ).annotate(like_count=Count("likes"))
        return Response(analytics, status=status.HTTP_200_OK)


class UserActivityView(generics.RetrieveAPIView):
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        user_activity, _ = UserActivity.objects.get_or_create(user=user)
        user_activity.last_request = timezone.now()
        user_activity.save()
        return user_activity
