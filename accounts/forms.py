from django import forms
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, UsernameField)
from django.utils.translation import gettext_lazy as _
from .models import User

class RegisterForm(UserCreationForm):
    """Form for user registration.

    Extends Django's UserCreationForm to include email and password confirmation fields.

    Args:
        UserCreationForm (class form): Django User Creation form.
    """
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'
    }))

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    password2 = forms.CharField(
        label='Confirm Password', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        """Meta class for RegisterForm.

        Specifies the model, fields, and widgets for the form.

        Args:
            model (class): User model.
            fields (list): Fields to include in form.
            widgets (dict): Widgets for form.
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(
            label=_('Password'), strip=False,
            widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
