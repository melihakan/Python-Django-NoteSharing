from ckeditor.widgets import CKEditorWidget
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea, FileInput

#from content.models import Content


# class ContactFormu(ModelForm):
#     class Meta:
#         model = Content
#         fields = ['title','slug','keywords','description','image','file','detail']
#         widgets = {
#             'title'   : TextInput(attrs={'class': 'input','placeholder':'title'}),
#             'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
#             'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
#             'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
#
#             'image' : FileInput(attrs={'class': 'input','placeholder':'Subject'}),
#             'file'   : FileInput(attrs={'class': 'input','placeholder':'Email Address'}),
#             'detail' : CKEditorWidget()
#         }