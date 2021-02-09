from django import forms
from .models import Show


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'
