from django.contrib.auth.models import User


class WidgetFrameworkAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        return True

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
