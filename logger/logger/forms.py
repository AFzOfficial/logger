from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Log


class LogForm(forms.ModelForm):
    body = forms.CharField(max_length=200, required=True, widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Whats Happening?!",
            "rows": 3,
            "class": "log-form",
        }
    ),
        label=""
    )

    class Meta():
        model = Log
        exclude = ("user", )


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(label='', widget=forms.TextInput(
    #     attrs={
    #         'class': '',
    #         'placeholder': 'Email'
    #     }
    # ))

    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'sign-up-inputs',
            'placeholder': 'First name'
        }
    ),
        help_text=''
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'sign-up-inputs'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['class'] = 'sign-up-inputs'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'sign-up-inputs'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''
