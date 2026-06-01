import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class ProductCategory(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("نشط")
        INACTIVE = "inactive", _("غير نشط")

    merchant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_categories",
        verbose_name=_("التاجر"),
    )
    name = models.CharField(max_length=120, verbose_name=_("الاسم"))
    slug = models.SlugField(max_length=140, blank=True, verbose_name=_("الرابط"))
    description = models.TextField(blank=True, verbose_name=_("الوصف"))
    icon = models.CharField(max_length=64, blank=True, verbose_name=_("الأيقونة"))
    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_("الحالة"),
    )
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("الترتيب"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("تصنيف")
        verbose_name_plural = _("التصنيفات")
        ordering = ["sort_order", "name"]
        constraints = [
            UniqueConstraint(
                fields=["merchant", "slug"],
                name="uniq_category_slug_per_merchant",
            )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base = slugify(self.name) or str(uuid.uuid4())[:8]
        qs = ProductCategory.objects.filter(merchant=self.merchant)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        candidate = base[:140]
        counter = 1
        while qs.filter(slug=candidate).exists():
            suffix = f"-{counter}"
            candidate = base[: 140 - len(suffix)] + suffix
            counter += 1
        return candidate


class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "Active", _("نشط")
        DRAFT = "Draft", _("مسودة")
        DISABLED = "Disabled", _("معطّل")

    class Badge(models.TextChoices):
        BESTSELLER = "Bestseller", _("الأكثر مبيعاً")
        NEW = "New", _("جديد")
        HOT_OFFER = "Hot Offer", _("عرض ساخن")
        HIGH_PROFIT = "High Profit", _("ربح مرتفع")
        NONE = "None", _("لا يوجد")

    class Currency(models.TextChoices):
        SAR = "SAR", _("ريال سعودي")
        EGP = "EGP", _("جنيه مصري")
        AED = "AED", _("درهم إماراتي")
        KWD = "KWD", _("دينار كويتي")
        USD = "USD", _("دولار أمريكي")

    merchant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("التاجر"),
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("التصنيف"),
    )
    name = models.CharField(max_length=200, verbose_name=_("الاسم"))
    slug = models.SlugField(max_length=220, blank=True, verbose_name=_("الرابط الداخلي"))
    short_description = models.CharField(
        max_length=300, blank=True, verbose_name=_("وصف مختصر")
    )
    description = models.TextField(blank=True, verbose_name=_("الوصف الكامل"))
    supplier_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("سعر المورد")
    )
    suggested_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("السعر المقترح")
    )
    affiliate_profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("عمولة المسوّق"),
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.EGP,
        verbose_name=_("العملة"),
    )
    stock_quantity = models.PositiveIntegerField(
        default=0, verbose_name=_("الكمية المتاحة")
    )
    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("الحالة"),
    )
    badge = models.CharField(
        max_length=12,
        choices=Badge.choices,
        default=Badge.NONE,
        verbose_name=_("الشارة"),
    )
    public_link_slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name=_("رابط الصفحة العامة"),
    )
    seo_title = models.CharField(max_length=60, blank=True, verbose_name=_("عنوان SEO"))
    seo_description = models.CharField(
        max_length=160, blank=True, verbose_name=_("وصف SEO")
    )
    video_url = models.URLField(blank=True, verbose_name=_("رابط الفيديو"))
    is_featured = models.BooleanField(default=False, verbose_name=_("منتج مميّز"))
    is_best_seller = models.BooleanField(default=False, verbose_name=_("الأكثر مبيعاً"))
    is_hot_offer = models.BooleanField(default=False, verbose_name=_("عرض ساخن"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("منتج")
        verbose_name_plural = _("المنتجات")
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["merchant", "slug"],
                name="uniq_product_slug_per_merchant",
            ),
            CheckConstraint(
                check=Q(supplier_price__gte=0),
                name="chk_product_supplier_price_non_negative",
            ),
            CheckConstraint(
                check=Q(suggested_price__gte=0),
                name="chk_product_suggested_price_non_negative",
            ),
            CheckConstraint(
                check=Q(affiliate_profit__gte=0) | Q(affiliate_profit__isnull=True),
                name="chk_product_affiliate_profit_non_negative",
            ),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if (
            self.affiliate_profit is None
            and self.suggested_price is not None
            and self.supplier_price is not None
        ):
            self.affiliate_profit = self.suggested_price - self.supplier_price

        if self.suggested_price is not None and self.supplier_price is not None:
            if self.suggested_price < self.supplier_price:
                raise ValidationError(
                    {
                        "suggested_price": _(
                            "السعر المقترح يجب أن يكون أكبر من أو يساوي سعر المورد."
                        )
                    }
                )

        if self.category_id and self.merchant_id:
            if not ProductCategory.objects.filter(
                pk=self.category_id, merchant_id=self.merchant_id
            ).exists():
                raise ValidationError(
                    {"category": _("يجب أن ينتمي التصنيف لنفس التاجر.")}
                )

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        if not self.public_link_slug:
            self.public_link_slug = self._generate_unique_public_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base = slugify(self.name) or str(uuid.uuid4())[:8]
        qs = Product.objects.filter(merchant=self.merchant)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        candidate = base[:220]
        counter = 1
        while qs.filter(slug=candidate).exists():
            suffix = f"-{counter}"
            candidate = base[: 220 - len(suffix)] + suffix
            counter += 1
        return candidate

    def _generate_unique_public_slug(self):
        base = slugify(self.name) or str(uuid.uuid4())[:8]
        qs = Product.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        candidate = base[:220]
        counter = 1
        while qs.filter(public_link_slug=candidate).exists():
            suffix = f"-{counter}"
            candidate = base[: 220 - len(suffix)] + suffix
            counter += 1
        return candidate


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("المنتج"),
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        verbose_name=_("الصورة"),
    )
    alt_text = models.CharField(
        max_length=200, blank=True, verbose_name=_("النص البديل")
    )
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("الترتيب"))
    is_main = models.BooleanField(default=False, verbose_name=_("الصورة الرئيسية"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("صورة منتج")
        verbose_name_plural = _("صور المنتجات")
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.name} — {self.sort_order}"

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(
                product=self.product, is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)
