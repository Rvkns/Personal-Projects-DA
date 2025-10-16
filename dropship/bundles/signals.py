"""Signals for automatically managing user profiles."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=get_user_model())
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Ensure each user has a corresponding profile."""
    if created:
        UserProfile.objects.create(user=instance, phone_number="")
    else:
        instance.profile.save()
