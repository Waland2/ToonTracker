from django import forms
from .models import Cartoons
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-input'}))  

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if 3 <= len(username) <= 25:
            return username
        raise forms.ValidationError('Логин должен содержать от 3 до 25 символов.')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Эта почта уже зарегистрована.')
        return email
        
    def clean_password2(self):
        cd = self.cleaned_data
        print(cd)
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        elif len(cd['password1']) < 6:
            raise forms.ValidationError('Пароль должен состоять минимум из 6 символов.')
        return cd['password2']
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    