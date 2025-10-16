"""Main URL configuration for the Dropship Bundles platform."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from bundles import views as bundle_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", bundle_views.HomeView.as_view(), name="home"),
    path("bundles/", include("bundles.urls")),
    path("accounts/signup/", bundle_views.SignUpView.as_view(), name="signup"),
    path("accounts/activate/<uidb64>/<token>/", bundle_views.ActivateAccountView.as_view(), name="activate"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url="/accounts/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/accounts/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
