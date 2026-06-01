from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from apps.core.decorators import role_required

from .forms import ProductForm
from .models import Product, ProductCategory
from .selectors import get_owned_product_or_404, list_products


@role_required("is_merchant")
def product_list(request):
    params = {
        "q": request.GET.get("q", ""),
        "category": request.GET.get("category", ""),
        "status": request.GET.get("status", ""),
        "badge": request.GET.get("badge", ""),
        "stock": request.GET.get("stock", ""),
    }
    qs = list_products(request.user, params)
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    qs_params = request.GET.copy()
    qs_params.pop("page", None)

    categories = ProductCategory.objects.filter(
        merchant=request.user, status=ProductCategory.Status.ACTIVE
    )
    return render(
        request,
        "products/product_list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "filters": params,
            "querystring": qs_params.urlencode(),
            "status_choices": Product.Status.choices,
            "badge_choices": Product.Badge.choices,
        },
    )


@role_required("is_merchant")
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, merchant=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.merchant = request.user
            product.save()
            return redirect("products:detail", slug=product.slug)
    else:
        form = ProductForm(merchant=request.user)
    return render(request, "products/product_form.html", {"form": form, "is_create": True})


# ── Stub views (replaced in later phases) ────────────────────────────────────


@role_required("is_merchant")
def product_detail(request, slug):
    product = get_owned_product_or_404(request.user, slug)
    images = list(product.images.all())
    return render(request, "products/product_detail.html", {
        "product": product,
        "images": images,
    })


@role_required("is_merchant")
def product_edit(request, slug):
    product = get_owned_product_or_404(request.user, slug)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product, merchant=request.user)
        if form.is_valid():
            form.save()
            return redirect("products:detail", slug=product.slug)
    else:
        form = ProductForm(instance=product, merchant=request.user)
    return render(
        request,
        "products/product_form.html",
        {"form": form, "is_create": False, "product": product},
    )


@role_required("is_merchant")
def product_disable(request, slug):
    return redirect("products:list")


@role_required("is_merchant")
def product_enable(request, slug):
    return redirect("products:list")


@role_required("is_merchant")
def product_duplicate(request, slug):
    return redirect("products:list")


@role_required("is_merchant")
def product_delete(request, slug):
    return redirect("products:list")
