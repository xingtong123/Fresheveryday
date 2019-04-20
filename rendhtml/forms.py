from django import forms
from django.core import  validators

class RegisTer(forms.Form):
    username=forms.CharField(validators=[
        validators.RegexValidator(regex='^\w{6,20}$',message='用户名不合法')
    ])
    password=forms.CharField(validators=[
        validators.RegexValidator(regex='^\w{6,30}$',message='密码不合法')
    ])
    password1 = forms.CharField(validators=[
        validators.RegexValidator(regex='^\w{6,30}$', message='密码不合法')
    ])
    # password1==password
    email=forms.EmailField()
