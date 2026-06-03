from django.urls import path
from .views import ContactEmailView, ContactListView

urlpatters = [
    path('contact/email/', ContactEmailView.as_view(), name='contact-email'),
    path('contact/list/', ContactListView.as_view(), name='contact-list'),
]