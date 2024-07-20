# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import logout
from item.models import Category, Item
from .forms import SignupForm
import random

from django.conf import settings
from django.core.mail import send_mail

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