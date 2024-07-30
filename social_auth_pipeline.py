from django.contrib.auth import get_user_model

def associate_by_email(backend, details, user=None, *args, **kwargs):
    User = get_user_model()
    if user:
        return {'user': user}

    # Ищем пользователя с данным email
    email = details.get('email')
    if email:
        try:
            user = User.objects.get(email=email)
            return {'user': user}
        except User.DoesNotExist:
            pass

    return None
