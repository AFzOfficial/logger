from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from .models import Log, Profile


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

    class Meta:
        model = Log
        exclude = ("user", "likes", 'replies', 'is_reply')


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(max_length=70, label='', help_text='', required=False,
                          widget=forms.widgets.TextInput(
                              attrs={
                                  'class': 'form-inputs',
                                  'placeholder': 'Bio'
                              }
                          ))

    photo = forms.ImageField(label='', help_text='',
                             widget=forms.widgets.FileInput(
                                 attrs={
                                     'class': 'file-input',
                                     'placeholder': 'Profile Photo'
                                 }
                             ))

    class Meta:
        model = Profile
        fields = ('bio', 'photo', )


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(label='', widget=forms.TextInput(
    #     attrs={
    #         'class': '',
    #         'placeholder': 'Email'
    #     }
    # ))

    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'form-inputs',
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

        self.fields['username'].widget.attrs['class'] = 'form-inputs'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['class'] = 'form-inputs'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'form-inputs'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''


class UpdateUserForm(UserChangeForm):

    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'form-inputs',
            'placeholder': 'First name'
        }
    ),
        help_text=''
    )

    class Meta:
        model = User
        fields = ('username', 'first_name')

        help_texts = {
            'username': None,
            'first_name': None,
        }

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-inputs'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''

        self.fields['password'].label = ''
        self.fields['password'].help_text = ''
