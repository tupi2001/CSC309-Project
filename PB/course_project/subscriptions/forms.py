from django import forms
from django.core.validators import MinLengthValidator

class Subscribe(forms.Form):
    name = forms.CharField(max_length=200)
    card = forms.CharField(max_length=23, validators=[MinLengthValidator(23)])
    subscription = forms.ChoiceField()

    def clean(self):
        data = super().clean()

        if not data.get('name'):
            self.add_error('name', 'This field is required')
        if not data.get('card'):
            self.add_error('card', 'This field is required')
        if not data.get('subscription'):
            self.add_error('subscription', 'This field is required')

class CardInformation(forms.Form):
    name = forms.CharField(max_length=200)
    card = forms.CharField(max_length=23, validators=[MinLengthValidator(23)])