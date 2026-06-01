from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.products.models import Product, ProductCategory, ProductImage
from apps.products.selectors import merchant_products, public_products


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


class ProductDisableTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m")
        self.cat = make_category(self.m)
        self.p = make_product(self.m, self.cat, status=Product.Status.ACTIVE)
        self.client.force_login(self.m)
        self.url = reverse("products:disable", kwargs={"slug": self.p.slug})

    def test_disable_sets_status(self):
        self.client.post(self.url)
        self.p.refresh_from_db()
        self.assertEqual(self.p.status, Product.Status.DISABLED)

    def test_disabled_excluded_from_public_products(self):
        self.client.post(self.url)
        self.p.refresh_from_db()
        self.assertNotIn(self.p, list(public_products(merchant_products(self.m))))

    def test_redirects_to_detail(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("products:detail", kwargs={"slug": self.p.slug}),
            fetch_redirect_response=False,
        )

    def test_cross_owner_returns_404(self):
        other = make_merchant("dis_other")
        other_p = make_product(other, make_category(other, "oc1"), name="Other Disable")
        response = self.client.post(reverse("products:disable", kwargs={"slug": other_p.slug}))
        self.assertEqual(response.status_code, 404)

    def test_get_returns_405(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url)
        self.assertEqual(response.status_code, 403)


class ProductEnableTests(TestCase):
    def setUp(self):
        self.m = make_merchant("me")
        self.cat = make_category(self.m)
        self.p = make_product(self.m, self.cat, status=Product.Status.DISABLED)
        self.client.force_login(self.m)
        self.url = reverse("products:enable", kwargs={"slug": self.p.slug})

    def test_enable_sets_status_to_active(self):
        self.client.post(self.url)
        self.p.refresh_from_db()
        self.assertEqual(self.p.status, Product.Status.ACTIVE)

    def test_redirects_to_detail(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("products:detail", kwargs={"slug": self.p.slug}),
            fetch_redirect_response=False,
        )

    def test_cross_owner_returns_404(self):
        other = make_merchant("en_other")
        other_p = make_product(other, make_category(other, "oc2"), name="Other Enable", status=Product.Status.DISABLED)
        response = self.client.post(reverse("products:enable", kwargs={"slug": other_p.slug}))
        self.assertEqual(response.status_code, 404)

    def test_get_returns_405(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url)
        self.assertEqual(response.status_code, 403)


class ProductDuplicateTests(TestCase):
    def setUp(self):
        self.m = make_merchant("md")
        self.cat = make_category(self.m)
        self.p = make_product(self.m, self.cat, "Original", status=Product.Status.ACTIVE)
        self.client.force_login(self.m)
        self.url = reverse("products:duplicate", kwargs={"slug": self.p.slug})

    def test_creates_new_draft_product(self):
        self.client.post(self.url)
        self.assertEqual(Product.objects.filter(merchant=self.m).count(), 2)
        copy = Product.objects.filter(merchant=self.m).exclude(pk=self.p.pk).first()
        self.assertEqual(copy.status, Product.Status.DRAFT)

    def test_copy_has_different_slug(self):
        self.client.post(self.url)
        copy = Product.objects.filter(merchant=self.m).exclude(pk=self.p.pk).first()
        self.assertNotEqual(copy.slug, self.p.slug)

    def test_copy_has_different_public_link_slug(self):
        self.client.post(self.url)
        copy = Product.objects.filter(merchant=self.m).exclude(pk=self.p.pk).first()
        self.assertNotEqual(copy.public_link_slug, self.p.public_link_slug)

    def test_copies_images(self):
        ProductImage.objects.create(product=self.p, alt_text="img1", is_main=True)
        self.client.post(self.url)
        copy = Product.objects.filter(merchant=self.m).exclude(pk=self.p.pk).first()
        self.assertEqual(copy.images.count(), 1)

    def test_redirects_to_copy_edit(self):
        response = self.client.post(self.url)
        copy = Product.objects.filter(merchant=self.m).exclude(pk=self.p.pk).first()
        self.assertRedirects(
            response,
            reverse("products:edit", kwargs={"slug": copy.slug}),
            fetch_redirect_response=False,
        )

    def test_cross_owner_returns_404(self):
        other = make_merchant("dup_other")
        other_p = make_product(other, make_category(other, "oc3"))
        response = self.client.post(reverse("products:duplicate", kwargs={"slug": other_p.slug}))
        self.assertEqual(response.status_code, 404)

    def test_get_returns_405(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url)
        self.assertEqual(response.status_code, 403)


class ProductDeleteTests(TestCase):
    def setUp(self):
        self.m = make_merchant("mdel")
        self.cat = make_category(self.m)
        self.p = make_product(self.m, self.cat)
        self.client.force_login(self.m)
        self.url = reverse("products:delete", kwargs={"slug": self.p.slug})

    def test_delete_removes_product(self):
        slug = self.p.slug
        self.client.post(self.url)
        self.assertFalse(Product.objects.filter(merchant=self.m, slug=slug).exists())

    def test_redirects_to_list(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("products:list"), fetch_redirect_response=False)

    def test_cross_owner_returns_404(self):
        other = make_merchant("del_other")
        other_p = make_product(other, make_category(other, "oc4"), name="Other Delete")
        response = self.client.post(reverse("products:delete", kwargs={"slug": other_p.slug}))
        self.assertEqual(response.status_code, 404)

    def test_get_returns_405(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url)
        self.assertEqual(response.status_code, 403)
