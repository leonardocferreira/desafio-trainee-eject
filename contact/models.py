from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name='Full Name')
    phone_number = models.CharField(max_length=14, verbose_name='Phone Number')
    email = models.EmailField(verbose_name='Email Address')
    subject = models.CharField(max_length=200, verbose_name='Subject')
    message = models.TextField(verbose_name='Message')

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-message']

    def __str__(self):
        return f'{self.name} - {self.subject}'