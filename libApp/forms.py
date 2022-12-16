from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Book
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
class book_form(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('book_name','author','book_types','book_cover','book_pdf')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control mb3 form-control-lg','placeholder':'Username','id':'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Password','id':'login-pwd'}
    ))

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Enter Username',min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100,help_text='Required',error_messages={
        'required':'Sorry, you will need an email'
    })
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat passowrd',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email')

    # To check whether they are unique

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username = username)
        if r.count():
            raise ValidationError('Username already exists')
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('Please use another Email, that is already taken')
        return email

    

