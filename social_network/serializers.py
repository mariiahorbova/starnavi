from rest_framework import serializers
from django.contrib.auth.models import User
from social_network.models import Post, UserActivity


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["user", "likes"]


class CustomPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ["likes"]


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name"
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
        return user


class AnalyticsSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    like_count = serializers.IntegerField()
