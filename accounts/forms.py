from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = "Passwords do not match"
            raise ValidationError(message)

        return password2


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserSubscriptionForm(forms.Form):
    MONTHS = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
        'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'
    ]
    CHOOSE_MONTH = list(enumerate(MONTHS, 1))
    CHOOSE_YEAR = [(i, i) for i in xrange(2017, 2038)]

    credit_card_number = forms.CharField(label='Credit card numer')
    cvv = forms.CharField(label='Security code (CVV)')
    expiry_month = forms.ChoiceField(label='Exp Month', choices=CHOOSE_MONTH)
    expiry_year = forms.ChoiceField(label='Exp Year', choices=CHOOSE_YEAR)
    stripe_id = forms.CharField(widget=forms.HiddenInput)

    class Meta:

        fields = ['stripe_id']
        exclude = ['username']


class UserPhotoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['avatar']
