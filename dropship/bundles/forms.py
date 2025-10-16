"""Forms for user registration and bundle management."""

from __future__ import annotations

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    """Collect user details including phone number for registration."""

    first_name = forms.CharField(label="Nome", max_length=30)
    last_name = forms.CharField(label="Cognome", max_length=30)
    email = forms.EmailField(label="Email")
    phone_number = forms.CharField(label="Numero di telefono", max_length=20)
    accept_terms = forms.BooleanField(
        label="Accetto i termini del servizio e l'informativa privacy",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-check-input"})
        self.fields["accept_terms"].widget.attrs.update({"class": "form-check-input"})
        self.fields["accept_terms"].label_suffix = ""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "username",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esiste già un account registrato con questa email.")
        return email

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        if commit:
            user.save()
            phone = self.cleaned_data["phone_number"].strip()
            profile = user.profile
            profile.phone_number = phone
            profile.save(update_fields=["phone_number"])
        return user
