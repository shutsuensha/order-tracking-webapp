from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('', views.items, name='items'),
    path('<int:pk>/add', views.add, name='add'),
    path('<int:pk>/remove', views.remove, name='remove'),
    path('basket/', views.basket, name='basket'),
]