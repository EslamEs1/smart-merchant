import uuid

from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .models import Product, ProductCategory
from .services import compute_affiliate_profit


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "short_description",
            "description",
            "supplier_price",
            "suggested_price",
            "affiliate_profit",
            "currency",
            "stock_quantity",
            "status",
            "badge",
            "public_link_slug",
            "seo_title",
            "seo_description",
            "video_url",
            "is_featured",
            "is_best_seller",
            "is_hot_offer",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "seo_description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, merchant=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.merchant = merchant
        if merchant is not None:
            self.fields["category"].queryset = ProductCategory.objects.filter(
                merchant=merchant, status=ProductCategory.Status.ACTIVE
            )
        self.fields["affiliate_profit"].required = False
        self.fields["public_link_slug"].required = False

    def clean_public_link_slug(self):
        value = (self.cleaned_data.get("public_link_slug") or "").strip()

        if not value:
            name = self.cleaned_data.get("name", "")
            base = slugify(name) or str(uuid.uuid4())[:8]
            qs = Product.objects.all()
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            candidate = base[:220]
            counter = 1
            while qs.filter(public_link_slug=candidate).exists():
                suffix = f"-{counter}"
                candidate = base[: 220 - len(suffix)] + suffix
                counter += 1
            return candidate

        qs = Product.objects.filter(public_link_slug=value)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                _("هذا الرابط مستخدم مسبقاً. يرجى اختيار رابط مختلف.")
            )
        return value

    def clean(self):
        cleaned_data = super().clean()
        supplier_price = cleaned_data.get("supplier_price")
        suggested_price = cleaned_data.get("suggested_price")
        affiliate_profit = cleaned_data.get("affiliate_profit")

        if (
            affiliate_profit is None
            and supplier_price is not None
            and suggested_price is not None
        ):
            cleaned_data["affiliate_profit"] = compute_affiliate_profit(
                suggested_price, supplier_price
            )

        if supplier_price is not None and suggested_price is not None:
            if supplier_price < 0:
                self.add_error(
                    "supplier_price", _("يجب أن تكون القيمة غير سالبة.")
                )
            if suggested_price < 0:
                self.add_error(
                    "suggested_price", _("يجب أن تكون القيمة غير سالبة.")
                )
            elif suggested_price < supplier_price:
                self.add_error(
                    "suggested_price",
                    _("السعر المقترح يجب أن يكون أكبر من أو يساوي سعر المورد."),
                )

        if affiliate_profit is not None and affiliate_profit < 0:
            self.add_error("affiliate_profit", _("يجب أن تكون القيمة غير سالبة."))

        category = cleaned_data.get("category")
        if category and self.merchant is not None:
            if category.merchant_id != self.merchant.pk:
                self.add_error(
                    "category", _("يجب أن ينتمي التصنيف لنفس التاجر.")
                )

        return cleaned_data
