from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.products.models import Product, ProductCategory


def make_user(username, role):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role=role
    )


def make_category(merchant, slug="cat"):
    return ProductCategory.objects.create(merchant=merchant, name=slug, slug=slug)


def make_product(merchant, cat, name, **kwargs):
    defaults = dict(supplier_price=10, suggested_price=20, affiliate_profit=10)
    defaults.update(kwargs)
    return Product.objects.create(merchant=merchant, category=cat, name=name, **defaults)


class ProductListAccessTests(TestCase):
    def setUp(self):
        self.url = reverse("products:list")
        self.merchant = make_user("m", "MERCHANT")
        self.affiliate = make_user("a", "AFFILIATE")
        self.cat = make_category(self.merchant)

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, f"/login.html?next={self.url}", fetch_redirect_response=False
        )

    def test_affiliate_gets_403(self):
        self.client.force_login(self.affiliate)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_merchant_gets_200(self):
        self.client.force_login(self.merchant)
        self.assertEqual(self.client.get(self.url).status_code, 200)


class ProductListOwnerScopeTests(TestCase):
    def setUp(self):
        self.url = reverse("products:list")
        self.ma = make_user("ma", "MERCHANT")
        self.mb = make_user("mb", "MERCHANT")
        self.cat_a = make_category(self.ma, "cat-a")
        self.cat_b = make_category(self.mb, "cat-b")
        self.pa = make_product(self.ma, self.cat_a, "Product A")
        self.pb = make_product(self.mb, self.cat_b, "Product B")

    def test_sees_own_products(self):
        self.client.force_login(self.ma)
        page = self.client.get(self.url).context["page_obj"]
        self.assertIn(self.pa, page.object_list)

    def test_does_not_see_other_merchant_products(self):
        self.client.force_login(self.ma)
        page = self.client.get(self.url).context["page_obj"]
        self.assertNotIn(self.pb, page.object_list)


class ProductListEmptyStateTests(TestCase):
    def test_zero_products_shows_empty_state(self):
        m = make_user("m0", "MERCHANT")
        make_category(m)
        client = self.client
        client.force_login(m)
        response = client.get(reverse("products:list"))
        self.assertEqual(response.context["page_obj"].paginator.count, 0)
        self.assertContains(response, "لا توجد منتجات")


class ProductListFilterTests(TestCase):
    def setUp(self):
        self.url = reverse("products:list")
        self.m = make_user("mf", "MERCHANT")
        self.cat = make_category(self.m)
        self.p_active = make_product(self.m, self.cat, "Active P", status=Product.Status.ACTIVE)
        self.p_draft = make_product(self.m, self.cat, "Draft P", status=Product.Status.DRAFT)
        self.client.force_login(self.m)

    def test_filter_status(self):
        page = self.client.get(self.url, {"status": "Active"}).context["page_obj"]
        self.assertIn(self.p_active, page.object_list)
        self.assertNotIn(self.p_draft, page.object_list)

    def test_filter_q(self):
        page = self.client.get(self.url, {"q": "Active P"}).context["page_obj"]
        self.assertIn(self.p_active, page.object_list)
        self.assertNotIn(self.p_draft, page.object_list)

    def test_no_match_shows_empty_count(self):
        page = self.client.get(self.url, {"q": "zzznomatch"}).context["page_obj"]
        self.assertEqual(page.paginator.count, 0)


class ProductListPaginationTests(TestCase):
    def test_paginates_at_12(self):
        m = make_user("mp", "MERCHANT")
        cat = make_category(m, "c")
        for i in range(15):
            make_product(m, cat, f"P{i}")
        self.client.force_login(m)
        page = self.client.get(reverse("products:list")).context["page_obj"]
        self.assertEqual(len(page.object_list), 12)
