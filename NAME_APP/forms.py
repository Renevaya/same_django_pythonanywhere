from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    def save(self):
        user = User(username = self.cleaned_data['username'],
                    email = self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username = username).exists():
            raise ValidationError("Пользователь с таким username уже существует")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())