from django.contrib.auth.forms import UserCreationForm
from kover.models import User
from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username']


class ProfileForm(forms.ModelForm):
    profileimg = forms.ImageField(required=False)  # 선택적으로 입력할 수 있음.
    nickname = forms.CharField(label='닉네임', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '8', }),
    )
    bio = forms.CharField(label='소개', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '30', }),
    )
    biolink = forms.CharField(label='사이트', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '30', }),
    )

    class Meta:
        model = Profile
        fields = ['nickname', 'profileimg', 'bio', 'biolink']
