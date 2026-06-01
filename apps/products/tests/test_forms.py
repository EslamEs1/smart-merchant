from decimal import Decimal

from django.test import TestCase

from apps.accounts.models import User
from apps.products.forms import ProductForm
from apps.products.models import Product, ProductCategory


def make_merchant(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="MERCHANT"
    )


def make_category(merchant, slug="cat"):
    return ProductCategory.objects.create(merchant=merchant, name=slug, slug=slug)


def base_data(category):
    return {
        "category": category.pk,
        "name": "Test Product",
        "short_description": "",
        "description": "",
        "supplier_price": "10.00",
        "suggested_price": "20.00",
        "affiliate_profit": "",
        "currency": "EGP",
        "stock_quantity": "5",
        "status": "Draft",
        "badge": "None",
        "public_link_slug": "",
        "seo_title": "",
        "seo_description": "",
        "video_url": "",
        "is_featured": False,
        "is_best_seller": False,
        "is_hot_offer": False,
    }


class ProductFormValidationTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m")
        self.cat = make_category(self.m)

    def test_valid_data_passes(self):
        form = ProductForm(data=base_data(self.cat), merchant=self.m)
        self.assertTrue(form.is_valid(), form.errors)

    def test_suggested_lt_supplier_fails(self):
        data = base_data(self.cat)
        data["suggested_price"] = "5.00"
        data["supplier_price"] = "10.00"
        form = ProductForm(data=data, merchant=self.m)
        self.assertFalse(form.is_valid())
        self.assertIn("suggested_price", form.errors)

    def test_negative_supplier_price_fails(self):
        data = base_data(self.cat)
        data["supplier_price"] = "-1.00"
        form = ProductForm(data=data, merchant=self.m)
        self.assertFalse(form.is_valid())

    def test_negative_suggested_price_fails(self):
        data = base_data(self.cat)
        data["suggested_price"] = "-1.00"
        form = ProductForm(data=data, merchant=self.m)
        self.assertFalse(form.is_valid())

    def test_negative_affiliate_profit_fails(self):
        data = base_data(self.cat)
        data["affiliate_profit"] = "-5.00"
        form = ProductForm(data=data, merchant=self.m)
        self.assertFalse(form.is_valid())
        self.assertIn("affiliate_profit", form.errors)

    def test_affiliate_profit_auto_filled_when_blank(self):
        data = base_data(self.cat)
        data["supplier_price"] = "10.00"
        data["suggested_price"] = "30.00"
        data["affiliate_profit"] = ""
        form = ProductForm(data=data, merchant=self.m)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["affiliate_profit"], Decimal("20.00"))

    def test_affiliate_profit_kept_when_provided(self):
        data = base_data(self.cat)
        data["affiliate_profit"] = "5.00"
        form = ProductForm(data=data, merchant=self.m)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["affiliate_profit"], Decimal("5.00"))

    def test_affiliate_profit_above_margin_fails(self):
        data = base_data(self.cat)
        data["supplier_price"] = "10.00"
        data["suggested_price"] = "20.00"  # margin = 10
        data["affiliate_profit"] = "15.00"  # exceeds margin
        form = ProductForm(data=data, merchant=self.m)
        self.assertFalse(form.is_valid())
        self.assertIn("affiliate_profit", form.errors)


class ProductFormSlugTests(TestCase):
    def setUp(self):
        self.m = make_merchant("ms")
        self.cat = make_category(self.m)

    def test_public_link_slug_auto_generated_from_name(self):
        data = base_data(self.cat)
        data["name"] = "ProBass X2"
        data["public_link_slug"] = ""
        form = ProductForm(data=data, merchant=self.m)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["public_link_slug"], "probass-x2")

    def test_public_link_slug_uniqueness_enforced(self):
        Product.objects.create(
            merchant=self.m, category=self.cat, name="Existing",
            supplier_price=10, suggested_price=20, affiliate_profit=10,
            public_link_slug="my-slug",
        )
        data = base_data(self.cat)
        data["public_link_slug"] = "my-slug"
        form = ProductForm(data=data, merchant=self.m)
        self.assertFalse(form.is_valid())
        self.assertIn("public_link_slug", form.errors)

    def test_public_link_slug_uniqueness_excludes_self_on_edit(self):
        p = Product.objects.create(
            merchant=self.m, category=self.cat, name="Existing",
            supplier_price=10, suggested_price=20, affiliate_profit=10,
            public_link_slug="my-slug",
        )
        data = base_data(self.cat)
        data["public_link_slug"] = "my-slug"
        form = ProductForm(data=data, instance=p, merchant=self.m)
        self.assertTrue(form.is_valid(), form.errors)

    def test_auto_slug_appends_suffix_on_collision(self):
        Product.objects.create(
            merchant=self.m, category=self.cat, name="ProBass X2",
            supplier_price=10, suggested_price=20, affiliate_profit=10,
            public_link_slug="probass-x2",
        )
        data = base_data(self.cat)
        data["name"] = "ProBass X2"
        data["public_link_slug"] = ""
        form = ProductForm(data=data, merchant=self.m)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["public_link_slug"], "probass-x2-1")


class ProductFormCategoryScopeTests(TestCase):
    def test_category_queryset_scoped_to_merchant(self):
        m1 = make_merchant("m1")
        m2 = make_merchant("m2")
        cat1 = make_category(m1, "cat-m1")
        cat2 = make_category(m2, "cat-m2")
        form = ProductForm(merchant=m1)
        qs = form.fields["category"].queryset
        self.assertIn(cat1, qs)
        self.assertNotIn(cat2, qs)

    def test_inactive_category_excluded(self):
        m = make_merchant("mi")
        cat_active = make_category(m, "active-cat")
        cat_inactive = ProductCategory.objects.create(
            merchant=m, name="Inactive", slug="inactive",
            status=ProductCategory.Status.INACTIVE,
        )
        form = ProductForm(merchant=m)
        qs = form.fields["category"].queryset
        self.assertIn(cat_active, qs)
        self.assertNotIn(cat_inactive, qs)

    def test_cross_merchant_category_rejected(self):
        m1 = make_merchant("cm1")
        m2 = make_merchant("cm2")
        cat2 = make_category(m2, "cat-c2")
        data = base_data(cat2)
        data["category"] = cat2.pk
        form = ProductForm(data=data, merchant=m1)
        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)
