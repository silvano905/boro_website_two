from django import forms
from .models import MakePost
from django.forms import Textarea, TextInput, ImageField


class MakePostForm(forms.ModelForm):

    class Meta:
        model = MakePost
        fields = ['title', 'post_pic', 'info']

        widgets = {
            'info': Textarea(attrs={'cols': 140, 'rows': 6, 'placeholder': 'info'}),
            'title': TextInput(attrs={'size': '55'})
        }