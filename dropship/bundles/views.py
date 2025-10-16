"""Views for the Dropship Bundles platform."""

from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import DetailView, FormView, ListView, TemplateView, View

from .forms import SignUpForm
from .models import Bundle


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["featured_bundles"] = Bundle.objects.filter(is_featured=True)[:3]
        context["recent_bundles"] = Bundle.objects.order_by("-created_at")[:6]
        return context


class BundleListView(ListView):
    model = Bundle
    context_object_name = "bundles"
    template_name = "bundles/bundle_list.html"
    paginate_by = 9


class BundleDetailView(DetailView):
    model = Bundle
    context_object_name = "bundle"
    template_name = "bundles/bundle_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class SignUpView(FormView):
    """Handle user registration and send activation email."""

    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")

    def form_valid(self, form: SignUpForm) -> HttpResponse:
        user: User = form.save(commit=False)
        user.is_active = False
        user.save()
        phone = form.cleaned_data["phone_number"].strip()
        profile = user.profile
        profile.phone_number = phone
        profile.email_confirmed = False
        profile.save(update_fields=["phone_number", "email_confirmed"])
        self.send_activation_email(user)
        messages.success(
            self.request,
            "Iscrizione completata! Ti abbiamo inviato un'email con il link di attivazione.",
        )
        return super().form_valid(form)

    def send_activation_email(self, user: User) -> None:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        protocol = "https" if settings.USE_HTTPS else "http"
        activation_url = f"{protocol}://{settings.SITE_DOMAIN}{reverse('activate', args=[uid, token])}"
        context = {
            "user": user,
            "activation_url": activation_url,
        }
        subject = "Conferma la tua registrazione su Dropship Bundles"
        message = render_to_string("emails/activation_email.txt", context)
        html_message = render_to_string("emails/activation_email.html", context)
        user.email_user(subject, message, html_message=html_message)


class ActivateAccountView(View):
    """Validate activation link and enable user account."""

    def get(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields=["is_active"])
            user.profile.mark_email_confirmed()
            login(request, user)
            messages.success(request, "Il tuo account è stato attivato con successo!")
            return redirect("bundles:bundle_list")
        messages.error(
            request,
            "Link di attivazione non valido o già utilizzato. Controlla di aver usato il link corretto.",
        )
        return redirect("home")
