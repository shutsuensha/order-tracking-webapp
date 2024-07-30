from django.dispatch import receiver
from social_core.pipeline.social_auth import social_user
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth
from social_core.exceptions import AuthAlreadyAssociated

@receiver(social_user)
def prevent_duplicate_accounts(backend, uid, user=None, *args, **kwargs):
    User = get_user_model()
    # Получаем email из данных
    email = kwargs.get('details', {}).get('email')
    if email:
        try:
            # Пытаемся найти пользователя с этим email
            existing_user = User.objects.get(email=email)
            if user and existing_user != user:
                raise AuthAlreadyAssociated(backend, existing_user)
            elif not user:
                return {'user': existing_user}
        except User.DoesNotExist:
            pass
