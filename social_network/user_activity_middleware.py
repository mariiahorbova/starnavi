from django.utils import timezone
from .models import UserActivity


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_activity, _ = UserActivity.objects.get_or_create(user=request.user)
            user_activity.last_request = timezone.now()
            user_activity.save()

        response = self.get_response(request)

        return response
