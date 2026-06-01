from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.products.models import Product, ProductCategory

User = get_user_model()

_CATEGORIES = [
    {"name": "إلكترونيات", "slug": "electronics", "sort_order": 1},
    {"name": "إكسسوارات موبايل", "slug": "mobile-accessories", "sort_order": 2},
    {"name": "أجهزة منزلية صغيرة", "slug": "small-home-appliances", "sort_order": 3},
    {"name": "عناية شخصية", "slug": "personal-care", "sort_order": 4},
    {"name": "ملابس", "slug": "clothing", "sort_order": 5},
    {"name": "أدوات منزلية", "slug": "home-tools", "sort_order": 6},
]

# public_link_slug is intentionally omitted — the model auto-generates a
# globally-unique value on save(), so two merchants seeded with the same
# product slugs never collide on this field.
_PRODUCTS = [
    {
        "name": "سماعة بلوتوث ProBass X2",
        "slug": "probass-x2",
        "category_slug": "electronics",
        "supplier_price": Decimal("150.00"),
        "suggested_price": Decimal("299.00"),
        "affiliate_profit": Decimal("149.00"),
        "stock_quantity": 45,
        "status": Product.Status.ACTIVE,
        "badge": Product.Badge.BESTSELLER,
        "short_description": "سماعة بلوتوث لاسلكية بصوت عالي الجودة",
    },
    {
        "name": "ساعة ذكية FitTime S9",
        "slug": "fittime-s9",
        "category_slug": "electronics",
        "supplier_price": Decimal("400.00"),
        "suggested_price": Decimal("699.00"),
        "affiliate_profit": Decimal("299.00"),
        "stock_quantity": 30,
        "status": Product.Status.ACTIVE,
        "badge": Product.Badge.NEW,
        "short_description": "ساعة ذكية بشاشة AMOLED ومتابعة اللياقة البدنية",
    },
    {
        "name": "كاميرا مراقبة WiFi 360",
        "slug": "wifi-cam-360",
        "category_slug": "electronics",
        "supplier_price": Decimal("280.00"),
        "suggested_price": Decimal("499.00"),
        "affiliate_profit": Decimal("219.00"),
        "stock_quantity": 15,
        "status": Product.Status.DRAFT,
        "badge": Product.Badge.NONE,
        "short_description": "كاميرا مراقبة ذكية بزاوية 360 درجة",
    },
    {
        "name": "باور بانك 20000mAh",
        "slug": "powerbank-20000",
        "category_slug": "mobile-accessories",
        "supplier_price": Decimal("100.00"),
        "suggested_price": Decimal("199.00"),
        "affiliate_profit": Decimal("99.00"),
        "stock_quantity": 80,
        "status": Product.Status.ACTIVE,
        "badge": Product.Badge.HIGH_PROFIT,
        "short_description": "باور بانك سعة 20000mAh بشحن سريع",
    },
    {
        "name": "شاحن سريع Type-C 65W",
        "slug": "fast-charger-65w",
        "category_slug": "mobile-accessories",
        "supplier_price": Decimal("60.00"),
        "suggested_price": Decimal("129.00"),
        "affiliate_profit": Decimal("69.00"),
        "stock_quantity": 120,
        "status": Product.Status.ACTIVE,
        "badge": Product.Badge.HOT_OFFER,
        "short_description": "شاحن GaN سريع 65W بمنفذ Type-C",
    },
    {
        "name": "Ring Light للموبايل",
        "slug": "ring-light-mobile",
        "category_slug": "mobile-accessories",
        "supplier_price": Decimal("120.00"),
        "suggested_price": Decimal("199.00"),
        "affiliate_profit": Decimal("79.00"),
        "stock_quantity": 0,
        "status": Product.Status.DISABLED,
        "badge": Product.Badge.NONE,
        "short_description": "إضاءة حلقية للموبايل لتصوير المحتوى",
    },
    {
        "name": "قلاية هوائية 4 لتر",
        "slug": "air-fryer-4l",
        "category_slug": "small-home-appliances",
        "supplier_price": Decimal("350.00"),
        "suggested_price": Decimal("599.00"),
        "affiliate_profit": Decimal("249.00"),
        "stock_quantity": 25,
        "status": Product.Status.ACTIVE,
        "badge": Product.Badge.BESTSELLER,
        "short_description": "قلاية هوائية صحية سعة 4 لتر بدون زيت",
    },
    {
        "name": "ماكينة حلاقة كهربائية",
        "slug": "electric-shaver",
        "category_slug": "personal-care",
        "supplier_price": Decimal("200.00"),
        "suggested_price": Decimal("349.00"),
        "affiliate_profit": Decimal("149.00"),
        "stock_quantity": 40,
        "status": Product.Status.ACTIVE,
        "badge": Product.Badge.NONE,
        "short_description": "ماكينة حلاقة كهربائية مقاومة للماء",
    },
    {
        "name": "شنطة ظهر ضد المياه",
        "slug": "waterproof-backpack",
        "category_slug": "clothing",
        "supplier_price": Decimal("120.00"),
        "suggested_price": Decimal("229.00"),
        "affiliate_profit": Decimal("109.00"),
        "stock_quantity": 35,
        "status": Product.Status.ACTIVE,
        "badge": Product.Badge.NEW,
        "short_description": "حقيبة ظهر مقاومة للماء بسعة 30 لتر",
    },
    {
        "name": "هودي شتوي Oversize",
        "slug": "oversized-hoodie",
        "category_slug": "clothing",
        "supplier_price": Decimal("80.00"),
        "suggested_price": Decimal("159.00"),
        "affiliate_profit": Decimal("79.00"),
        "stock_quantity": 60,
        "status": Product.Status.DRAFT,
        "badge": Product.Badge.NONE,
        "short_description": "هودي شتوي أوفر سايز من القطن الناعم",
    },
    {
        "name": "منظم أدراج متعدد الاستخدام",
        "slug": "drawer-organizer",
        "category_slug": "home-tools",
        "supplier_price": Decimal("45.00"),
        "suggested_price": Decimal("89.00"),
        "affiliate_profit": Decimal("44.00"),
        "stock_quantity": 150,
        "status": Product.Status.ACTIVE,
        "badge": Product.Badge.HOT_OFFER,
        "short_description": "منظم أدراج مرن بمقسمات قابلة للتعديل",
    },
    {
        "name": "ستاند لابتوب قابل للطي",
        "slug": "laptop-stand",
        "category_slug": "home-tools",
        "supplier_price": Decimal("70.00"),
        "suggested_price": Decimal("149.00"),
        "affiliate_profit": Decimal("79.00"),
        "stock_quantity": 55,
        "status": Product.Status.ACTIVE,
        "badge": Product.Badge.HIGH_PROFIT,
        "short_description": "ستاند لابتوب ألومنيوم قابل للطي مع 6 مستويات ارتفاع",
    },
]


class Command(BaseCommand):
    help = "Seed demo physical-commerce categories and products (idempotent)."

    def handle(self, *args, **options):
        merchant = self._get_or_create_merchant()
        categories = self._seed_categories(merchant)
        self._seed_products(merchant, categories)
        self.stdout.write(self.style.SUCCESS("seed_products completed successfully."))

    def _get_or_create_merchant(self):
        merchant = (
            User.objects.filter(role="MERCHANT", is_staff=False, is_superuser=False).first()
            or User.objects.filter(role="MERCHANT").first()
        )
        if merchant:
            self.stdout.write(f"Using existing merchant: {merchant.email}")
            return merchant

        merchant = User.objects.create_user(
            username="demo_merchant",
            email="demo@merchant.com",
            password="demo1234",
            role="MERCHANT",
        )
        self.stdout.write(
            self.style.WARNING(
                f"Created demo merchant: {merchant.email}  password: demo1234"
            )
        )
        return merchant

    def _seed_categories(self, merchant):
        category_map = {}
        for data in _CATEGORIES:
            cat, created = ProductCategory.objects.get_or_create(
                merchant=merchant,
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "sort_order": data["sort_order"],
                    "status": ProductCategory.Status.ACTIVE,
                },
            )
            if created:
                self.stdout.write(f"  Created category: {cat.name}")
            category_map[data["slug"]] = cat
        return category_map

    def _seed_products(self, merchant, categories):
        for data in _PRODUCTS:
            category = categories.get(data["category_slug"])
            if not category:
                self.stderr.write(
                    f"  Skipped product '{data['name']}': "
                    f"category '{data['category_slug']}' not found"
                )
                continue

            _, created = Product.objects.get_or_create(
                merchant=merchant,
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "category": category,
                    "short_description": data["short_description"],
                    "supplier_price": data["supplier_price"],
                    "suggested_price": data["suggested_price"],
                    "affiliate_profit": data["affiliate_profit"],
                    "stock_quantity": data["stock_quantity"],
                    "status": data["status"],
                    "badge": data["badge"],
                },
            )
            if created:
                self.stdout.write(f"  Created product: {data['name']}")
