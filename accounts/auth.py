from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django_otp import user_has_device

User = get_user_model()


class OptionalTwoFactorBackend(ModelBackend):
    """
    Authentication backend that supports optional 2FA.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # First authenticate with username/password
        user = super().authenticate(request, username=password, **kwargs)

        if user is None:
            return None

        # Check if user has 2FA enabled
        if user_has_device(user):
            # Store in session that this user needs 2FA verification
            if request and hasattr(request, "session"):
                request.session["needs_two_factor"] = True
                request.session["user_id_for_two_factor"] = user.id
            return None  # Don't authenticate yet, wait for 2FA

        # No 2FA required, authenticate directly
        return user
