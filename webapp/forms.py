from django import forms
from webapp.models import User, Question
from django.db.models import Q
from django.utils.text import slugify

class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class UserResgistrationForm(forms.ModelForm):
    password2 = forms.CharField(
        min_length=8,
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )
    password = forms.CharField(
        min_length=8,
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
            }
        ),
    )
    def __init__(self, *args, **kwargs):
        super(UserResgistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password'].label = 'Password'

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    @staticmethod
    def cleanfield(data):
        return str(data).strip().lower()

    def clean(self):
        cd = self.cleaned_data
        if User.objects.filter(
            Q(username=self.cleanfield(cd["username"]))
            | Q(email=self.cleanfield(cd["email"]))
        ).exists():
            raise forms.ValidationError("Username Already Exists!!")

        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords Doesn't match!!")


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'description')

    def clean_question_text(self):
        question_text = self.cleaned_data.get("question_text")
        if Question.objects.filter(question_slug=slugify(question_text)).exists():
            raise forms.ValidationError("Question Already Exists!!")
        return question_text
