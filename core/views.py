# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import logout, login
from item.models import Category, Item
from .forms import SignupForm
import random

from django.conf import settings
from django.core.mail import send_mail

from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from social_django.utils import psa
from google.oauth2 import id_token
from google.auth.transport import requests
import json

@psa('social:complete')
def google_one_tap_login(request, backend):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('credential')

        try:
            # Проверка токена
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)
            email = idinfo['email']
        except ValueError:
            # Невалидный токен
            return JsonResponse({'success': False}, status=400)

        # Аутентификация пользователя через PSA
        user = request.backend.do_auth(token)
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': settings.LOGIN_REDIRECT_URL})
        else:
            return JsonResponse({'success': False}, status=401)
    else:
        return JsonResponse({'success': False}, status=405)


def index(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    gender = ''
    if "gender" not in request.session:
        gender = 'ALL'
    else:
        gender = request.session["gender"]

    if gender != 'ALL':
        items = items.filter(gender=gender)

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': sorted(items, key=lambda x: random.random()),
        'name_category' : '🪦💀',
        'gender': gender
    })


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    items = Item.objects.filter(category=category)
    categories = Category.objects.all()

    gender = ''
    if "gender" not in request.session:
        gender = 'ALL'
    else:
        gender = request.session["gender"]

    if gender != 'ALL':
        items = items.filter(gender=gender)

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': sorted(items, key=lambda x: random.random()),
        'name_category' : category.name,
        'gender': gender,
        'query': category
    })  


def log_out(request):
    logout(request)
    return redirect('/login/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            subject = 'Nyashki store'
            message = f'Спасибо за регистрацию'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form['email'].value()]
            send_mail( subject, message, email_from, recipient_list )

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })