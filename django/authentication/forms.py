from django.forms import ModelForm
from django import forms
from authentication.models import User
import django.contrib.auth.password_validation as validators
from django.core.validators import ValidationError
from django.core import exceptions


class SignupForm(ModelForm):
    password = forms.CharField(max_length=100)
    confirm_password = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].unique = True

        self.fields['password'].required = True
        self.fields['confirm_password'].required = True

        self.fields['username'].required = True
        self.fields['username'].unique = True

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'user_type']
        widgets = {
            'password': forms.PasswordInput({"class": "form-control", "placeholder":"Password"}),
            'confirm_password': forms.PasswordInput({"class": "form-control", "placeholder": "Confirm Password"}),
            'email': forms.EmailInput({"class": "form-control", "placeholder":"Email"}),
            'username': forms.TextInput({"class": "form-control", "placeholder":"Username"}),
            'first_name': forms.TextInput({"class": "form-control", "placeholder": "FirstName"}),
            'last_name': forms.TextInput({"class": "form-control", "placeholder": "LastName"}),
        }
        help_texts = {
            'password': '* Password must be at least 6 characters long',
            'username': '* Username must be blah blah blah',
        }

    def clean(self):
        """
        Validate user input and clean
        :return:
        """
        super().clean()
        data = self.cleaned_data

        if data["password"] != data["confirm_password"]:
            self._errors["password"] = 'Password mismatch'
            self._errors["confirm_password"] = 'Password mismatch'

            raise ValidationError("Password mismatch")

        data["password"] = data["password"]

        try:
            validators.validate_password(data["password"])
        except exceptions.ValidationError as e:
            raise ValidationError(list(e.messages))

        del data["password"]
        del data["confirm_password"]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput({"class": "form-control", "placeholder":"Username"}),
        max_length=80,
        label="Username",
        required=True
    )

    password = forms.CharField(
        widget=forms.PasswordInput({"class": "form-control", "placeholder":"Password"}),
        label="Password",
        required=True
    )