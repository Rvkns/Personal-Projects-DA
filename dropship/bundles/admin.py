"""Admin configuration for bundles app."""

from django.contrib import admin

from .models import Bundle, BundleItem, UserProfile


class BundleItemInline(admin.TabularInline):
    model = BundleItem
    extra = 1


@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ("name", "price_eur", "is_featured", "created_at")
    list_filter = ("is_featured",)
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BundleItemInline]


@admin.register(BundleItem)
class BundleItemAdmin(admin.ModelAdmin):
    list_display = ("title", "bundle", "source_name", "price_eur")
    search_fields = ("title", "source_name")
    list_filter = ("bundle",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "email_confirmed", "created_at")
    list_filter = ("email_confirmed",)
    search_fields = ("user__username", "user__email", "phone_number")
