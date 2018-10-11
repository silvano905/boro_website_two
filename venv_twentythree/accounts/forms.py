from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea, TextInput

class UserFormRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserFormProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'description', 'profile_pic')


# -------------------------to update---------------------------------------

class UserFormProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'profile_pic']

        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 4}),
        }


class UserFormCreationFormUpdate(forms.ModelForm):
    User._meta.get_field('email')._unique = True
    User._meta.get_field('username')._unique = True

    class Meta:
        model = User
        fields = ('username',)

        widgets = {
            'username': TextInput(attrs={'size': '20'})
        }