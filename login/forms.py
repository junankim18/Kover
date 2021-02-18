from django.contrib.auth.forms import UserCreationForm
from kover.models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username']
