from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import SMAUser, UserProfile


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
<<<<<<< HEAD
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'password')
=======
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
>>>>>>> d4f7942bfde3bcea95aae21d7379a8027cf01bfe

    def __init__(self, *args, **kwargs):
        super(SMAUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
<<<<<<< HEAD

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data

class SMAUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'vk_username')

    def __init__(self, *args, **kwargs):
        super(SMAUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
=======
>>>>>>> d4f7942bfde3bcea95aae21d7379a8027cf01bfe
