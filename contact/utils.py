from django.core.mail import send_mail
from django.conf import settings

def send_contact_email(contact):
    subject = f'Contact: {contact.subject}'
    message = (
        f'Name: {contact.name}\n'
        f'Phone: {contact.phone_number}\n'
        f'Email: {contact.email}\n'
        f'Message: {contact.message}'
    )

    from_email = [settings.DEFAULT_FROM_EMAIL]
    recipient_list = [settings.DEFAULT_FROM_EMAIL]
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
