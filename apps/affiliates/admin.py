from django.contrib import admin

from .models import AffiliateProfile


@admin.register(AffiliateProfile)
class AffiliateProfileAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "merchant",
        "level",
        "status",
        "referral_code",
        "coupon_code",
        "created_at",
    ]
    list_filter = ["status", "level"]
    search_fields = ["full_name", "email", "phone", "referral_code", "coupon_code"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "approved_at",
        "rejected_at",
        "suspended_at",
    ]
