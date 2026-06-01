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


def edit_url(slug):
    return reverse("products:edit", kwargs={"slug": slug})


def valid_post(cat):
    return {
        "category": cat.pk,
        "name": "Updated Name",
        "short_description": "",
        "description": "",
        "supplier_price": "10.00",
        "suggested_price": "25.00",
        "affiliate_profit": "15.00",
        "currency": "EGP",
        "stock_quantity": "5",
        "status": "Active",
        "badge": "None",
        "public_link_slug": "",
        "seo_title": "",
        "seo_description": "",
        "video_url": "",
    }


class ProductEditAccessTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m")
        self.cat = make_category(self.m)
        self.p = make_product(self.m, self.cat)

    def test_anonymous_redirects_to_login(self):
        url = edit_url(self.p.slug)
        response = self.client.get(url)
        self.assertRedirects(response, f"/login.html?next={url}", fetch_redirect_response=False)

    def test_merchant_sees_own_product_form(self):
        self.client.force_login(self.m)
        self.assertEqual(self.client.get(edit_url(self.p.slug)).status_code, 200)

    def test_cross_merchant_get_returns_404(self):
        other = make_merchant("other")
        other_cat = make_category(other, "other-cat")
        other_p = make_product(other, other_cat, name="Other P")
        self.client.force_login(self.m)
        self.assertEqual(self.client.get(edit_url(other_p.slug)).status_code, 404)

    def test_cross_merchant_post_returns_404(self):
        other = make_merchant("other2")
        other_cat = make_category(other, "oc2")
        other_p = make_product(other, other_cat, name="Other P2")
        self.client.force_login(self.m)
        response = self.client.post(edit_url(other_p.slug), valid_post(self.cat))
        self.assertEqual(response.status_code, 404)


class ProductEditPreFillTests(TestCase):
    def setUp(self):
        self.m = make_merchant("mf")
        self.cat = make_category(self.m)
        self.p = make_product(
            self.m, self.cat, "Original Name",
            status=Product.Status.ACTIVE, stock_quantity=42,
        )
        self.client.force_login(self.m)

    def test_get_shows_current_product_name(self):
        response = self.client.get(edit_url(self.p.slug))
        self.assertContains(response, "Original Name")

    def test_get_shows_correct_stock_value(self):
        response = self.client.get(edit_url(self.p.slug))
        self.assertContains(response, "42")

    def test_form_not_is_create(self):
        response = self.client.get(edit_url(self.p.slug))
        self.assertFalse(response.context["is_create"])
        self.assertEqual(response.context["product"], self.p)


class ProductEditPersistTests(TestCase):
    def setUp(self):
        self.m = make_merchant("mp")
        self.cat = make_category(self.m)
        self.p = make_product(self.m, self.cat, "Old Name")
        self.client.force_login(self.m)

    def test_valid_post_updates_product(self):
        data = valid_post(self.cat)
        data["name"] = "New Name"
        self.client.post(edit_url(self.p.slug), data)
        self.p.refresh_from_db()
        self.assertEqual(self.p.name, "New Name")

    def test_valid_post_redirects_to_detail(self):
        response = self.client.post(edit_url(self.p.slug), valid_post(self.cat))
        self.assertRedirects(
            response,
            reverse("products:detail", kwargs={"slug": self.p.slug}),
            fetch_redirect_response=False,
        )

    def test_invalid_pricing_does_not_save(self):
        data = valid_post(self.cat)
        data["suggested_price"] = "5.00"
        data["supplier_price"] = "20.00"
        self.client.post(edit_url(self.p.slug), data)
        self.p.refresh_from_db()
        self.assertEqual(self.p.name, "Old Name")

    def test_invalid_post_re_renders_form(self):
        data = valid_post(self.cat)
        data["suggested_price"] = "5.00"
        data["supplier_price"] = "20.00"
        response = self.client.post(edit_url(self.p.slug), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)


class ProductEditSlugUniquenessTests(TestCase):
    def setUp(self):
        self.m = make_merchant("msu")
        self.cat = make_category(self.m)
        self.p = make_product(self.m, self.cat, "P1", public_link_slug="my-slug")
        self.client.force_login(self.m)

    def test_can_save_with_own_slug(self):
        data = valid_post(self.cat)
        data["public_link_slug"] = "my-slug"
        response = self.client.post(edit_url(self.p.slug), data)
        self.assertRedirects(
            response,
            reverse("products:detail", kwargs={"slug": self.p.slug}),
            fetch_redirect_response=False,
        )

    def test_cannot_use_another_product_slug(self):
        other = make_product(self.m, self.cat, "P2", public_link_slug="other-slug")
        data = valid_post(self.cat)
        data["public_link_slug"] = "other-slug"
        response = self.client.post(edit_url(self.p.slug), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("public_link_slug", response.context["form"].errors)
