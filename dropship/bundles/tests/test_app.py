from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from bundles.models import Bundle


class BundleModelTests(TestCase):
    def test_slug_created_automatically(self):
        bundle = Bundle.objects.create(
            name="Postazione Gaming",
            short_description="Setup completo per gamer",
            description="Dettagli",
            price_eur=999.99,
        )
        self.assertEqual(bundle.slug, "postazione-gaming")

    def test_get_absolute_url(self):
        bundle = Bundle.objects.create(
            name="Starter Streaming",
            short_description="Setup entry-level",
            description="",
            price_eur=499.00,
        )
        self.assertEqual(bundle.get_absolute_url(), reverse("bundles:bundle_detail", args=[bundle.slug]))


class AccountFlowTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_creates_inactive_user_and_sends_activation(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "first_name": "Mario",
                "last_name": "Rossi",
                "email": "mario@example.com",
                "phone_number": "+391234567890",
                "username": "marior",
                "password1": "SuperSegreta123",
                "password2": "SuperSegreta123",
                "accept_terms": True,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username="marior")
        self.assertFalse(user.is_active)
        self.assertFalse(user.profile.email_confirmed)
        self.assertEqual(user.profile.phone_number, "+391234567890")

    def test_activation_enables_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Testpass123",
            is_active=False,
        )
        user.profile.phone_number = "+3900000000"
        user.profile.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        response = self.client.get(reverse("activate", args=[uid, token]), follow=True)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.profile.email_confirmed)
        self.assertRedirects(response, reverse("bundles:bundle_list"))
