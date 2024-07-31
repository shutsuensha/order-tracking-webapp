from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from .models import Category, Item, Purchase, Comment

import random

from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .forms import NewItemForm, NewCategoryForm, EditItemForm, EditCategoryForm, NewCommentForm



def detail(request, pk, operation=None, form=None, pk_comment=None, form_edit=None, op=None, js_op=None):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)

    gender = ''
    if "gender" not in request.session:
        gender = 'ALL'
    else:
        gender = request.session["gender"]

    if gender != 'ALL':
        related_items = related_items.filter(gender=gender)


    if request.user.is_authenticated:
        basket_items = request.user.items.all()
        in_basket = False
        if item in basket_items:
            in_basket = True

        if form == None:
            form = NewCommentForm()
        
        return render(request, 'item/detail.html', {
            'item': item,
            'related_items': related_items,
            'in_basket': in_basket,
            'operation': operation,
            'gender': gender,
            'form': form,
            'edit_form': form_edit,
            'pk_comment': pk_comment,
            'op': op,
            'js_op': js_op
        })

    return render(request, 'item/detail.html', {
            'item': item,
            'related_items': related_items,
            'gender': gender
    })

def items(request):
    query = request.GET.get('query', '')
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    gender = ''
    if "gender" not in request.session:
        gender = 'ALL'
    else:
        gender = request.session["gender"]

    if gender != 'ALL':
        items = items.filter(gender=gender)

    if query:
        items = items.filter(Q(name__contains=query) | Q(description__contains=query) | Q(category__name__contains=query))

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': sorted(items, key=lambda x: random.random()),
        'name_category' : f'{query}' if query else '🪦💀',
        'gender': gender,
        'query': query
    })

@login_required
def add(request, pk):
    item = get_object_or_404(Item, pk=pk)
    request.user.items.add(item)
    return detail(request, pk=pk, operation="add", js_op='fgkjsdflkgjdkslfg')

@login_required
def basket(request, message=None):
    items = request.user.items.all()
    purchases = Purchase.objects.filter(user=request.user)

    gender = ''
    if "gender" not in request.session:
        gender = 'ALL'
    else:
        gender = request.session["gender"]

    if gender != 'ALL':
        items = items.filter(gender=gender)

    

    return render(request, 'item/basket.html', {
        'items': items,
        'gender': gender,
        'message': message,
        'purchases': purchases
    })

@login_required
def remove(request, pk):
    item = get_object_or_404(Item, pk=pk)
    request.user.items.remove(item)
    return redirect('item:basket')

@login_required
def remove_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    request.user.items.remove(item)
    return detail(request, pk=pk, operation="remove", js_op='fgkjsdflkgjdkslfg')


def gender_f(request, gender):
    if "gender" not in request.session:
        request.session["gender"] = ''
    request.session["gender"] = gender
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
def gender_detail_f(request, gender, pk):
    if "gender" not in request.session:
        request.session["gender"] = ''
    request.session["gender"] = gender
    return redirect('item:detail', pk=pk)   

@login_required
def delete(request):
    request.user.items.clear()
    return redirect('item:basket')

@login_required
def purchase(request):
    purchase = Purchase.objects.create(user=request.user, telegram=request.POST['telegram'], price=0)
    price = 0
    if request.user.items.all():
        for item in request.user.items.all():
            price += item.price
            purchase.items.add(item)
        purchase.price = price  
        purchase.save()
        request.user.items.clear()


        context = {
            'purchase': purchase
        }
        template_name = "item/email_purchase.html"

        convert_to_html_content =  render_to_string(
            template_name=template_name,
            context=context
        )

        plain_message = strip_tags(convert_to_html_content)

        yo_send_it = send_mail(
            subject="Nyshki store",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],   # recipient_list is self explainatory
            html_message=convert_to_html_content,
            fail_silently=True
        )

        import requests

        bot_username = 'nyshaka_bot'
        bot_api = settings.BOT_API
        channel_name = '@nyashki_orders'
        message = convert_to_html_content
        url = f'https://api.telegram.org/bot{bot_api}/sendMessage'
        params = {
            'chat_id': channel_name,
            'text': convert_to_html_content,
            'parse_mode': 'HTML'  # Устанавливаем режим HTML
        }

        response = requests.get(url, params=params)

        return basket(request, 'Заказ успешно оформлен) c вами свяжиться АДМИН))))админ пидарас')
    return basket(request, 'в корзине пусто')


@login_required
def purchase_delete(request, pk):
    instance = Purchase.objects.get(id=pk)
    subject = 'Nyashki store'
    message = f'Вы удалили заказ, все потому что админ пидарас'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email]
    send_mail( subject, message, email_from, recipient_list )
    import requests
    bot_username = 'nyshaka_bot'
    bot_api = settings.BOT_API
    channel_name = '@nyashki_orders'
    message = f'заказ для {instance.telegram}, price: {instance.price}$ УДАЛЕН'
    url = f'https://api.telegram.org/bot{bot_api}/sendMessage?chat_id={channel_name}&text={message}'
    requests.get(url)
    instance.delete()

    return redirect('item:basket')


@login_required
def all_purchases(request):
    if request.user.is_superuser:
        return render(request, 'item/purchases.html', {
            "purchases": Purchase.objects.all()
        })
    else:
        return redirect('/')
    

@login_required
def new_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = NewCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = NewCategoryForm()
        return render(request, 'item/new_category_form.html', {
            'form': form,
            'title': 'New Category',
        })
            
    else:
        return redirect('/')
    


@login_required
def new_item(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            print('123')
            form = NewItemForm(request.POST, request.FILES)

            if form.is_valid():
                item = form.save(commit=False)
                item.created_by = request.user
                item.save()

                return redirect('item:detail', pk=item.id)
        else:
            form = NewItemForm()

        return render(request, 'item/new_item_form.html', {
            'form': form,
            'title': 'New item',
        })
            
    else:
        return redirect('/')
    

@login_required
def remove_item(request, pk):
    if request.user.is_superuser:
        instance = Item.objects.get(id=pk)
        instance.delete()
    return redirect('/')
    

@login_required
def remove_category(request, pk):
    if request.user.is_superuser:
        instance = Category.objects.get(id=pk)
        instance.delete()
    return redirect('/')


@login_required
def edit_item(request, pk):
    if request.user.is_superuser:
        item = get_object_or_404(Item, pk=pk)

        if request.method == 'POST':
            form = EditItemForm(request.POST, request.FILES, instance=item)

            if form.is_valid():
                form.save()

                return redirect('item:detail', pk=item.id)
        else:
            form = EditItemForm(instance=item)

        return render(request, 'item/edit_item_form.html', {
            'form': form,
            'title': 'Edit item',
            'item': item
        })
    return redirect('/')


@login_required
def edit_category(request, pk):
    if request.user.is_superuser:
        category = get_object_or_404(Category, pk=pk)

        if request.method == 'POST':
            form = EditCategoryForm(request.POST, request.FILES, instance=category)

            if form.is_valid():
                form.save()

                return redirect('/')
        else:
            form = EditCategoryForm(instance=category)

        return render(request, 'item/edit_category_form.html', {
            'form': form,
            'title': 'Edit category',
            'category': category
        })
    return redirect('/')

@login_required
def new_comment(request, pk):
    if request.method == 'POST':
            item = Item.objects.get(pk=pk)
            form = NewCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.created_at = datetime.now()
                comment.save()
                item.comments.add(comment)
                return detail(request, pk=pk, op='comments')
            
            return detail(request, pk, form=form, op='comments')

    return redirect('/')

@login_required
def delete_comment(request, pk_comment, pk_item):
    comment = Comment.objects.get(pk=pk_comment)
    if request.user == comment.user:
        comment.delete()
        return detail(request, pk=pk_item, op='comments')
    return redirect('item:detail', pk=pk_item)


@login_required
def edit_comment(request, pk_comment, pk_item):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=pk_comment)
        form = NewCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_at = datetime.now()
            comment.save()
            return detail(request, pk_item, op='comments')
        return detail(request, pk_item, pk_comment=pk_comment, form_edit=form, op='comments')

    else:
        comment = Comment.objects.get(pk=pk_comment)
        if not request.user == comment.user:
            return redirect('item:detail', pk=pk_item)
        edit_form = NewCommentForm(instance=comment)
        return detail(request, pk_item, pk_comment=pk_comment, form_edit=edit_form, op='comments')
    

@login_required
def all_comments(request):
    items = Item.objects.filter(comments__user=request.user).distinct()
    return render(request, 'item/comments.html', {
            'items': items
    })
