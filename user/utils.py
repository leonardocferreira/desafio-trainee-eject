from django.db import models

class RoleChoice(models.TextChoices):
    CUSTUMER = 'c', 'Custumer'
    SHOPKEEPER = 's', 'Shopkeeper'