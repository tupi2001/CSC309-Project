from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    

    def clean(self):
        cleaned_data = super().clean()

        if not (user := authenticate(username=cleaned_data.get('username'), password=cleaned_data.get('password'))):
            self.add_error('password', 'Username or Password is invalid')


        cleaned_data['user'] = user

        return cleaned_data