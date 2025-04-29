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
    include_numbers = forms.BooleanField(required=False)
    include_special = forms.BooleanField(required=False)
    include_similar = forms.BooleanField(required=False)

    class Meta:
        model = Password
        fields = ['app_name', 'url', 'username', 'app_type']
        widgets = {
            'app_type': forms.Select(),
        }

class PasswordUpdateForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ['app_name', 'url', 'username', 'app_pass', 'app_type']
        widgets = {
            'app_pass': forms.PasswordInput(),
            'app_type': forms.Select(),
        }

        def __init__ (self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['app_name'].disabled = False
            self.fields['url'].disabled = False
            self.fields['username'].disabled = False
            self.fields['app_type'].disabled = False
    