from django import forms
from webapp.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class UserResgistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'