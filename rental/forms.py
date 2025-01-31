from django import forms
from .models import Car
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return password_confirm

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'price_per_day', 'image']
