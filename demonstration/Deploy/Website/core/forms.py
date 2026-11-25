from django import forms
from .models import DocModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class DocumentForm(forms.ModelForm):
    class Meta:
        model = DocModel
        fields = ('vid', )


from . models import UserImageModel
class UserImageForm(forms.ModelForm):

    class Meta:
        model = UserImageModel
        fields = ['image']

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']