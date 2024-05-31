from django.dispatch import receiver
from django.db.models.signals import post_save
from katisha import settings
from .models import Passenger


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_passenger_for_new_user(sender, instance, created, **kwargs):
    if created:
        Passenger.objects.create(user=instance)