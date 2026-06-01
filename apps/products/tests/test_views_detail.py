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


def make_product(merchant, cat, name="Product", **kwargs):
    defaults = dict(supplier_price=10, suggested_price=20, affiliate_profit=10)
    defaults.update(kwargs)
    return Product.objects.create(merchant=merchant, category=cat, name=name, **defaults)


def detail_url(slug):
    return reverse("products:detail", kwargs={"slug": slug})


class ProductDetailAccessTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m")
        self.cat = make_category(self.m)
        self.p = make_product(self.m, self.cat)

    def test_anonymous_redirects_to_login(self):
        url = detail_url(self.p.slug)
        response = self.client.get(url)
        self.assertRedirects(response, f"/login.html?next={url}", fetch_redirect_response=False)

    def test_merchant_gets_200(self):
        self.client.force_login(self.m)
        self.assertEqual(self.client.get(detail_url(self.p.slug)).status_code, 200)

    def test_cross_merchant_returns_404(self):
        other = make_merchant("other")
        other_cat = make_category(other, "oc")
        other_p = make_product(other, other_cat, "Other P")
        self.client.force_login(self.m)
        self.assertEqual(self.client.get(detail_url(other_p.slug)).status_code, 404)


class ProductDetailContentTests(TestCase):
    def setUp(self):
        self.m = make_merchant("mc")
        self.cat = make_category(self.m, "electronics")
        self.p = make_product(
            self.m, self.cat, "ProBass X2",
            suggested_price="299.00", supplier_price="150.00",
            affiliate_profit="149.00", stock_quantity=45,
            status=Product.Status.ACTIVE,
        )
        self.client.force_login(self.m)

    def test_product_name_rendered(self):
        response = self.client.get(detail_url(self.p.slug))
        self.assertContains(response, "ProBass X2")

    def test_suggested_price_rendered(self):
        response = self.client.get(detail_url(self.p.slug))
        self.assertContains(response, "299")

    def test_category_name_rendered(self):
        response = self.client.get(detail_url(self.p.slug))
        self.assertContains(response, "electronics")

    def test_stock_rendered(self):
        response = self.client.get(detail_url(self.p.slug))
        self.assertContains(response, "45")

    def test_public_link_slug_rendered(self):
        response = self.client.get(detail_url(self.p.slug))
        self.assertContains(response, self.p.public_link_slug)

    def test_sales_summary_shows_zero(self):
        response = self.client.get(detail_url(self.p.slug))
        self.assertContains(response, "وحدات مباعة")

    def test_orders_empty_state_rendered(self):
        response = self.client.get(detail_url(self.p.slug))
        self.assertContains(response, "لا توجد طلبات مرتبطة")

    def test_context_has_product(self):
        response = self.client.get(detail_url(self.p.slug))
        self.assertEqual(response.context["product"], self.p)

    def test_edit_link_uses_clean_url(self):
        response = self.client.get(detail_url(self.p.slug))
        edit_url = reverse("products:edit", kwargs={"slug": self.p.slug})
        self.assertContains(response, edit_url)
