from django import forms
from post_bugs.models import CustUser, Post


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class EditForm(forms.Form):
    title = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.Textarea)
