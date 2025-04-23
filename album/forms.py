from django import forms
from .models import Album, Photo, Video
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video', 'description']


class AssignToAlbumForm(forms.Form):
    album = forms.ModelChoiceField(queryset=Album.objects.all())
    media_type = forms.ChoiceField(
        choices=[('photo', 'Зображення'), ('video', 'Відео')])
    media_id = forms.IntegerField(widget=forms.HiddenInput())


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
