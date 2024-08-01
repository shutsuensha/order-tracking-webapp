from django import forms

from .models import Item, Category, Comment

INPUT_CLASSES = 'block md:w-1/2 mx-auto py-4 px-6 rounded-xl border dark:bg-zinc-700 dark:text-white'

class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('description',)
        widgets = {
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
        }

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold', 'gender')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'gender': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
        }


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            })
        }
