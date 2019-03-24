from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import SMAUser


class SMAUserLoginForm(AuthenticationForm):
    class Meta:
        model = SMAUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(SMAUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SMAUserRegisterForm(UserCreationForm):
    class Meta:
        model = SMAUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super(SMAUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class SMAUserEditForm(UserChangeForm):
    class Meta:
        model = SMAUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(SMAUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

