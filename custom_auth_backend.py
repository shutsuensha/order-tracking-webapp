from social_core.backends.base import BaseAuth
from django.contrib.auth import get_user_model

class CustomAuthBackend(BaseAuth):
    def authenticate(self, *args, **kwargs):
        User = get_user_model()
        email = kwargs.get('email')
        if email:
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
