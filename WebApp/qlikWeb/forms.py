from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserForm(forms.Form):
    userName = forms.CharField(
        max_length=50,
        dsceswidget=forms.TextInput(attrs={'placeholder':'Username'}),
    )
    password = forms.CharField(
        label="Password", 
        strip= False, 
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}),
    )
