from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from content.models import Content, Category
from home.models import UserProfile



class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'first_name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'last_name' }),
        }

CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city','country','image')
        widgets = {
            'phone'     : TextInput(attrs={'class': 'input','placeholder':'phone'}),
            'address'   : TextInput(attrs={'class': 'input','placeholder':'address'}),
            'city'      : Select(attrs={'class': 'input','placeholder':'city'},choices=CITY),
            'country'   : TextInput(attrs={'class': 'input','placeholder':'country' }),
            'image'     : FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }

class UserNotesForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('title', 'keywords', 'description','image','file','detail','category','slug')
        widgets = {
            'title'     : TextInput(attrs={'class': 'input','placeholder':'title'}),
            'keywords'   : TextInput(attrs={'class': 'input','placeholder':'keywords'}),
            'description'      : TextInput(attrs={'class': 'input','placeholder':'description'}),
            'detail'   : TextInput(attrs={'class': 'input','placeholder':'detail' }),
            'image'     : FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
            'file': FileInput(attrs={'class': 'input', 'placeholder': 'file', }),
            'category': Select(attrs={'class': 'input','placeholder':'category' },choices=Category.objects.all()),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
        }



