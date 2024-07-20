from django.contrib import admin

from .models import Category, Item, Purchase, Comment

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Purchase)
admin.site.register(Comment)