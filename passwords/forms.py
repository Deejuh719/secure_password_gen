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
        fields = ['app_name', 'url', 'username']

# TODO: Make this like... idk... update the damn passwords?? replace them.... that thing
class PasswordUpdateForm(forms.ModelForm):
    length = forms.IntegerField(
        label="Password Length",
        min_value=12,
        max_value=32,
        initial=12,
    )
    include_numbers = forms.BooleanField(required=False)
    include_special = forms.BooleanField(required=False)
    include_similar = forms.BooleanField(required=False)
    class Meta:
        model = Password
        fields = ['app_name', 'url', 'username', 'app_pass']
        widgets = {
            'app_pass': forms.PasswordInput(),
        }

        def __init__ (self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['app_name'].disabled = True
            self.fields['url'].disabled = True
            self.fields['username'].disabled = True

    """def clean_password(self):
        app_pass = self.cleaned_data['app_pass']
        if len(app_pass) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return app_pass
    def clean_app_name(self):
        app_name = self.cleaned_data['app_name']
        if len(app_name) > 100:
            raise forms.ValidationError("App/Site Name must be 100 characters or less.")
        return app_name

    def clean_url(self):
        url = self.cleaned_data['url']
        if url and not url.startswith('http://') and not url.startswith('https://'):
            raise forms.ValidationError("URL must start with http:// or https://")
        return url"""
    