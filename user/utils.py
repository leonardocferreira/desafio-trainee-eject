from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlencode, urlsafe_base64_encode

def send_reset_email(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    query_params = urlencode({'uidb64': uidb64, 'token': token})
    base_url = settings.FRONTEND_URL.rstrip('/')
    link_reset = f'{base_url}/reset-password-confirm?{query_params}'
    
    subject='Password Reset Request'
    message=f'To request a password change, click the link to change it: {link_reset} \n\nIf you haven\'t requested one, ignore the email.'
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
