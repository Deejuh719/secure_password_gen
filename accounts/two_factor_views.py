from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from  django.contrib.auth import login, get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64


def setup_2fa(request):
    """View to set up 2FA for a user"""
    # Check if user already has 2FA
    if TOTPDevice.objects.filter(user=request.user, confirmed=True).exists():
        messages.info(request, "Two-factor authentication is already enabled.")
        return redirect("account_settings")

    # Create a new TOTP device if one doesn't exist
    device, created = TOTPDevice.objects.get_or_create(
        user=request.user, confirmed=False, defaults={"name": "default"}
    )

    if created:
        device.key = random_hex()
        device.save()

    # Generate QR code
    totp_url = device.config_url
    qr = qrcode.make(totp_url, image_factory=qrcode.image.svg.SvgImage)
    stream = BytesIO()
    qr.save(stream)
    qr_code = base64.b64encode(stream.getvalue()).decode()

    if request.method == "POST":
        token = request.POST.get("token")

        if device.verify_token(token):
            # Token is valid, confirm the device
            device.confirmed = True
            device.save()
            messages.success(request, "Two-factor authentication has been enabled.")
            return redirect("account_settings")
        else:
            messages.error(request, "Invalid verification code. Please try again.")

    return render(
        request,
        "accounts/setup_2fa.html",
        {
            "qr_code": qr_code,
            "secret_key": device.key,
        },
    )


def verify_2fa(request):
    user_id = request.session.get("user_id")

    if "user_id_for_2fa" not in request.session:
        messages.info(request, "Please log in first.")
        return redirect("login")

    if not user_id:
        messages.error(request, "Please log in first.")
        return redirect("login")

    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect("login")

    if request.method == "POST":
        token = request.POST.get("token")

        try:
            device = TOTPDevice.objects.filter(user=user).first()

            if device.verify_token(token):
                login(request, user)

                if 'user_id_for_2fa' in request.session:
                    del request.session['user_id_for_2fa']
                    return redirect("home")
            else:
                messages.error(request, "Invalid verification code. Please try again.")

        except TOTPDevice.DoesNotExist:
            messages.error(request, "No OTP device found for this user.")
            return redirect("login")

    return render(request, "accounts/verify_2fa.html")


@login_required
def disable_2fa(request):
    """View to disable 2FA for a user"""
    if request.method == "POST":
        # Delete all TOTP devices for the user
        TOTPDevice.objects.filter(user=request.user).delete()
        messages.success(request, "Two-factor authentication has been disabled.")
        return redirect("account_settings")

    return render(request, "accounts/disable_2fa.html")
