from django.test import TestCase

from apps.accounts.models import User
from apps.products.models import Product, ProductCategory
from apps.products.selectors import list_products, merchant_products, public_products


def make_merchant(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="MERCHANT"
    )


def make_category(merchant, slug):
    return ProductCategory.objects.create(merchant=merchant, name=slug, slug=slug)


def make_product(merchant, category, name, **kwargs):
    defaults = dict(supplier_price=10, suggested_price=20, affiliate_profit=10)
    defaults.update(kwargs)
    return Product.objects.create(merchant=merchant, category=category, name=name, **defaults)


class MerchantProductsTests(TestCase):
    def setUp(self):
        self.ma = make_merchant("a")
        self.mb = make_merchant("b")
        self.cat_a = make_category(self.ma, "cat-a")
        self.cat_b = make_category(self.mb, "cat-b")
        self.pa = make_product(self.ma, self.cat_a, "Product A", status=Product.Status.ACTIVE)
        self.pb = make_product(self.mb, self.cat_b, "Product B", status=Product.Status.ACTIVE)

    def test_isolation(self):
        qs = merchant_products(self.ma)
        self.assertIn(self.pa, qs)
        self.assertNotIn(self.pb, qs)

    def test_public_excludes_draft(self):
        draft = make_product(self.ma, self.cat_a, "Draft P", status=Product.Status.DRAFT)
        self.assertNotIn(draft, public_products(merchant_products(self.ma)))

    def test_public_excludes_disabled(self):
        disabled = make_product(self.ma, self.cat_a, "Dis P", status=Product.Status.DISABLED)
        self.assertNotIn(disabled, public_products(merchant_products(self.ma)))

    def test_public_includes_active(self):
        self.assertIn(self.pa, public_products(merchant_products(self.ma)))


class ListProductsFilterTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m")
        self.cat = make_category(self.m, "electronics")
        self.cat2 = make_category(self.m, "clothing")
        self.p1 = make_product(self.m, self.cat, "ProBass X2", status=Product.Status.ACTIVE, stock_quantity=5)
        self.p2 = make_product(self.m, self.cat2, "Hoodie", status=Product.Status.DRAFT, stock_quantity=0)

    def _filter(self, **kwargs):
        defaults = dict(q="", category="", status="", badge="", stock="")
        defaults.update(kwargs)
        return list(list_products(self.m, defaults))

    def test_no_filters_returns_all(self):
        results = self._filter()
        self.assertIn(self.p1, results)
        self.assertIn(self.p2, results)

    def test_filter_q_name(self):
        results = self._filter(q="ProBass")
        self.assertIn(self.p1, results)
        self.assertNotIn(self.p2, results)

    def test_filter_q_public_link_slug(self):
        self.p1.public_link_slug = "probass-x2"
        self.p1.save(update_fields=["public_link_slug"])
        results = self._filter(q="probass-x2")
        self.assertIn(self.p1, results)

    def test_filter_category(self):
        results = self._filter(category="electronics")
        self.assertIn(self.p1, results)
        self.assertNotIn(self.p2, results)

    def test_filter_status_active(self):
        results = self._filter(status="Active")
        self.assertIn(self.p1, results)
        self.assertNotIn(self.p2, results)

    def test_filter_status_draft(self):
        results = self._filter(status="Draft")
        self.assertNotIn(self.p1, results)
        self.assertIn(self.p2, results)

    def test_filter_badge(self):
        make_product(self.m, self.cat, "Bestseller P", badge=Product.Badge.BESTSELLER)
        results = self._filter(badge="Bestseller")
        names = [p.name for p in results]
        self.assertIn("Bestseller P", names)
        self.assertNotIn("ProBass X2", names)

    def test_filter_stock_in(self):
        results = self._filter(stock="in")
        self.assertIn(self.p1, results)
        self.assertNotIn(self.p2, results)

    def test_filter_stock_out(self):
        results = self._filter(stock="out")
        self.assertNotIn(self.p1, results)
        self.assertIn(self.p2, results)

    def test_combined_status_and_category(self):
        results = self._filter(status="Active", category="electronics")
        self.assertIn(self.p1, results)
        self.assertNotIn(self.p2, results)
