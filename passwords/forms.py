from django import forms


class PasswordGeneratorForm(forms.Form):
    app_name = forms.CharField(max_length=100, label="App/Site Name")
    length = forms.IntegerField(
        label="Password Length",
        min_value=8,
        max_value=32,
        initial=12,
    )
    include_uppercase = forms.BooleanField(required=False)
    include_numbers = forms.BooleanField(required=False)
    include_special = forms.BooleanField(required=False)
    include_similar_characters = forms.BooleanField(required=False)
