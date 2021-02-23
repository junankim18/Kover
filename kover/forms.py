from django import forms
from .models import Show, Feed_post


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'


class PostForm(forms.ModelForm):
    class Meta:
        model = Feed_post
        fields = '__all__'
