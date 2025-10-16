"""Database models for the Dropship Bundles platform."""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract model with created/modified tracking."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Bundle(TimeStampedModel):
    """A curated set of products that form a themed bundle."""

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    hero_image_url = models.URLField(blank=True)
    price_eur = models.DecimalField(max_digits=8, decimal_places=2)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Bundle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("bundles:bundle_detail", args=[self.slug])

    @property
    def total_items_price(self) -> float:
        return sum(item.price_eur for item in self.items.all())


class BundleItem(TimeStampedModel):
    """Individual product linked to an external supplier."""

    bundle = models.ForeignKey(Bundle, related_name="items", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    source_name = models.CharField(max_length=120)
    product_url = models.URLField()
    description = models.TextField(blank=True)
    price_eur = models.DecimalField(max_digits=8, decimal_places=2)
    thumbnail_url = models.URLField(blank=True)

    class Meta:
        ordering = ["bundle", "title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.source_name})"


class UserProfile(TimeStampedModel):
    """Stores additional information for platform users."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20)
    email_confirmed = models.BooleanField(default=False)
    activation_token_created_at = models.DateTimeField(null=True, blank=True)

    def mark_email_confirmed(self) -> None:
        self.email_confirmed = True
        self.activation_token_created_at = timezone.now()
        self.save(update_fields=["email_confirmed", "activation_token_created_at"])

    def __str__(self) -> str:
        return f"Profilo di {self.user.get_full_name() or self.user.username}"
