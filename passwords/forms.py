from django import forms
from .models import Password


class PasswordGeneratorForm(forms.ModelForm):
    app_name = forms.CharField(max_length=100, label="App/Site Name")
    url = forms.URLField(required=False)
    length = forms.IntegerField(
        label="Password Length",
        min_value=8,
        max_value=32,
        initial=12,
    )
    include_uppercase = forms.BooleanField(required=False)
    include_numbers = forms.BooleanField(required=False)
    include_special = forms.BooleanField(required=False)
    include_similar = forms.BooleanField(required=False)

    class Meta:
        model = Password
        fields = ['app_name', 'url', 'username']