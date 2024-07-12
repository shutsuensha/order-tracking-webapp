from django.db.models import Q
from django.shortcuts import render, get_object_or_404

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
        'name_category' : f'All girls for {query}'
    })