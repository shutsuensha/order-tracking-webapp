from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Item

import random

# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

def items(request):
    query = request.GET.get('query', '')
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if query:
        items = items.filter(Q(name__contains=query) | Q(description__contains=query) | Q(category__name__contains=query))

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': sorted(items, key=lambda x: random.random()),
        'name_category' : f'Вся одежда по 🔎 {query}' if query else 'Вся одежда 👕'
    })

@login_required
def add(request, pk):
    item = get_object_or_404(Item, pk=pk)
    request.user.items.add(item)
    return redirect('item:detail', pk=pk)

@login_required
def basket(request):
    return render(request, 'item/basket.html', {
        'items': request.user.items.all()
    })

@login_required
def remove(request, pk):
    item = get_object_or_404(Item, pk=pk)
    request.user.items.remove(item)
    return redirect('item:basket')