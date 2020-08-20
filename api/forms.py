from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        widgets = {'password': forms.PasswordInput(render_value=True)}
