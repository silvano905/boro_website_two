from django import forms
from .models import Todo
from django.forms import Textarea, TextInput, ImageField

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'todo_pic', 'info')

        widgets = {
            'info': Textarea(attrs={'cols': 144, 'rows': 6, 'placeholder': 'info'}),
            'title': TextInput(attrs={'size': '48'})
        }


class TestingForm(forms.Form):
    image = forms.ImageField()
