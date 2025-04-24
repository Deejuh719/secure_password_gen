from django import forms
from .models import Password


class PasswordGeneratorForm(forms.ModelForm):
    app_name = forms.CharField(max_length=100, label="App/Site Name")
    url = forms.URLField(required=False, help_text="Optional", widget=forms.URLInput(attrs={'placeholder': 'https://example.com'}))
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

class PasswordUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
    )
    class Meta:
        model = Password
        fields = ['app_name', 'url', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter new password'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance