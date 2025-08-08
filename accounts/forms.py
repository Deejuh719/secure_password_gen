from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "username", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords do not match")
        
        user = self.save(commit=False)
        try:
            validate_password(password2, user)
        except ValidationError as e:
            raise ValidationError(e.messages)
        
        return password2

class CustomUserChangeForm(UserChangeForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Current Password",
        required=True
    )
    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")
        return current_password
    
    """def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user""" # coded out to see if this helps anything, since it doesn't really do anything