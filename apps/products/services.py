from decimal import Decimal

from .models import Product, ProductImage


def compute_affiliate_profit(suggested_price: Decimal, supplier_price: Decimal) -> Decimal:
    return max(Decimal("0"), suggested_price - supplier_price)


def set_product_status(product: Product, status: str) -> None:
    product.status = status
    product.save(update_fields=["status", "updated_at"])


def duplicate_product(product: Product) -> Product:
    images = list(product.images.all())
    copy = Product(
        merchant=product.merchant,
        category=product.category,
        name=product.name,
        short_description=product.short_description,
        description=product.description,
        supplier_price=product.supplier_price,
        suggested_price=product.suggested_price,
        affiliate_profit=product.affiliate_profit,
        currency=product.currency,
        stock_quantity=product.stock_quantity,
        status=Product.Status.DRAFT,
        badge=product.badge,
        seo_title=product.seo_title,
        seo_description=product.seo_description,
        video_url=product.video_url,
        is_featured=product.is_featured,
        is_best_seller=product.is_best_seller,
        is_hot_offer=product.is_hot_offer,
    )
    copy.save()
    for img in images:
        ProductImage.objects.create(
            product=copy,
            image=img.image,
            alt_text=img.alt_text,
            sort_order=img.sort_order,
            is_main=img.is_main,
        )
    return copy
