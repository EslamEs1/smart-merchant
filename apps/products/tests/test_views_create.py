from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.products.models import Product, ProductCategory


def make_merchant(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="MERCHANT"
    )


def make_category(merchant, slug="cat"):
    return ProductCategory.objects.create(merchant=merchant, name=slug, slug=slug)


def valid_post(category):
    return {
        "category": category.pk,
        "name": "New Product",
        "short_description": "",
        "description": "",
        "supplier_price": "10.00",
        "suggested_price": "25.00",
        "affiliate_profit": "",
        "currency": "EGP",
        "stock_quantity": "10",
        "status": "Draft",
        "badge": "None",
        "public_link_slug": "",
        "seo_title": "",
        "seo_description": "",
        "video_url": "",
    }


class ProductCreateAccessTests(TestCase):
    def setUp(self):
        self.url = reverse("products:create")
        self.merchant = make_merchant("m")
        self.affiliate = make_user_affiliate()
        self.cat = make_category(self.merchant)

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/login.html?next={self.url}", fetch_redirect_response=False)

    def test_affiliate_gets_403(self):
        self.client.force_login(self.affiliate)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_merchant_gets_200(self):
        self.client.force_login(self.merchant)
        self.assertEqual(self.client.get(self.url).status_code, 200)


def make_user_affiliate():
    return User.objects.create_user(
        username="aff", email="aff@x.com", password="pass", role="AFFILIATE"
    )


class ProductCreateViewTests(TestCase):
    def setUp(self):
        self.url = reverse("products:create")
        self.m = make_merchant("mc")
        self.cat = make_category(self.m)
        self.client.force_login(self.m)

    def test_get_shows_blank_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_valid_post_creates_product(self):
        count_before = Product.objects.filter(merchant=self.m).count()
        self.client.post(self.url, valid_post(self.cat))
        self.assertEqual(Product.objects.filter(merchant=self.m).count(), count_before + 1)

    def test_merchant_set_from_request_not_post_data(self):
        other = make_merchant("other")
        data = valid_post(self.cat)
        self.client.post(self.url, data)
        p = Product.objects.filter(merchant=self.m).last()
        self.assertIsNotNone(p)
        self.assertEqual(p.merchant, self.m)

    def test_valid_post_redirects_to_detail(self):
        response = self.client.post(self.url, valid_post(self.cat))
        self.assertRedirects(
            response, reverse("products:detail", kwargs={"slug": Product.objects.filter(merchant=self.m).last().slug}),
            fetch_redirect_response=False,
        )

    def test_invalid_pricing_does_not_create_product(self):
        data = valid_post(self.cat)
        data["suggested_price"] = "5.00"
        data["supplier_price"] = "20.00"
        count_before = Product.objects.filter(merchant=self.m).count()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.filter(merchant=self.m).count(), count_before)

    def test_invalid_post_preserves_form_values(self):
        data = valid_post(self.cat)
        data["suggested_price"] = "5.00"
        data["supplier_price"] = "20.00"
        data["name"] = "Preserved Name"
        response = self.client.post(self.url, data)
        self.assertContains(response, "Preserved Name")

    def test_affiliate_profit_auto_filled(self):
        data = valid_post(self.cat)
        data["supplier_price"] = "10.00"
        data["suggested_price"] = "30.00"
        self.client.post(self.url, data)
        p = Product.objects.filter(merchant=self.m).last()
        self.assertEqual(p.affiliate_profit, 20)

    def test_public_link_slug_auto_generated(self):
        data = valid_post(self.cat)
        data["name"] = "AutoSlug Product"
        data["public_link_slug"] = ""
        self.client.post(self.url, data)
        p = Product.objects.filter(merchant=self.m).last()
        self.assertTrue(p.public_link_slug)
