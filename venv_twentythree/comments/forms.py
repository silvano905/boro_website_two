from django import forms
from .models import Comment, Suggestion


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }