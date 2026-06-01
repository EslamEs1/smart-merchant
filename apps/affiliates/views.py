from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.core.decorators import role_required

from . import services
from .forms import AffiliateChangeLevelForm, AffiliateNotesForm
from .models import AffiliateProfile
from .selectors import (
    get_owned_affiliate_or_404,
    list_affiliates,
    merchant_affiliates,
    pending_affiliates,
)


@role_required("is_merchant")
def affiliate_list(request):
    params = {
        "q": request.GET.get("q", ""),
        "status": request.GET.get("status", ""),
        "level": request.GET.get("level", ""),
    }
    qs = list_affiliates(request.user, params)
    paginator = Paginator(qs, 15)
    page_obj = paginator.get_page(request.GET.get("page"))

    qs_params = request.GET.copy()
    qs_params.pop("page", None)

    pending_count = pending_affiliates(merchant_affiliates(request.user)).count()

    return render(
        request,
        "affiliates/affiliate_list.html",
        {
            "page_obj": page_obj,
            "filters": params,
            "querystring": qs_params.urlencode(),
            "pending_count": pending_count,
            "status_choices": AffiliateProfile.Status.choices,
            "level_choices": AffiliateProfile.Level.choices,
        },
    )


@role_required("is_merchant")
def affiliate_requests(request):
    q = request.GET.get("q", "").strip()
    base_qs = pending_affiliates(merchant_affiliates(request.user))
    pending_count = base_qs.count()
    if q:
        base_qs = base_qs.filter(
            Q(full_name__icontains=q) | Q(referral_code__icontains=q)
        )

    return render(
        request,
        "affiliates/affiliate_requests.html",
        {
            "affiliates": base_qs,
            "q": q,
            "pending_count": pending_count,
        },
    )


@role_required("is_merchant")
@require_POST
def affiliate_approve(request, pk):
    affiliate = get_owned_affiliate_or_404(request.user, pk)
    services.approve(affiliate)
    messages.success(request, f"تم قبول {affiliate.full_name} كمسوّق.")
    return redirect("affiliates:requests")


@role_required("is_merchant")
@require_POST
def affiliate_reject(request, pk):
    affiliate = get_owned_affiliate_or_404(request.user, pk)
    reason = request.POST.get("reason", "").strip()
    services.reject(affiliate, reason=reason)
    messages.success(request, f"تم رفض طلب {affiliate.full_name}.")
    return redirect("affiliates:requests")


@role_required("is_merchant")
def affiliate_detail(request, pk):
    affiliate = get_owned_affiliate_or_404(request.user, pk)
    return render(request, "affiliates/affiliate_detail.html", {"affiliate": affiliate})


@role_required("is_merchant")
@require_POST
def affiliate_suspend(request, pk):
    affiliate = get_owned_affiliate_or_404(request.user, pk)
    reason = request.POST.get("reason", "").strip()
    services.suspend(affiliate, reason=reason)
    messages.success(request, f"تم إيقاف حساب {affiliate.full_name}.")
    return redirect("affiliates:detail", pk=affiliate.pk)


@role_required("is_merchant")
@require_POST
def affiliate_reactivate(request, pk):
    affiliate = get_owned_affiliate_or_404(request.user, pk)
    services.reactivate(affiliate)
    messages.success(request, f"تم إعادة تفعيل حساب {affiliate.full_name}.")
    return redirect("affiliates:detail", pk=affiliate.pk)


@role_required("is_merchant")
@require_POST
def affiliate_change_level(request, pk):
    affiliate = get_owned_affiliate_or_404(request.user, pk)
    form = AffiliateChangeLevelForm(request.POST)
    if form.is_valid():
        services.change_level(affiliate, form.cleaned_data["level"])
        messages.success(request, f"تم تغيير مستوى {affiliate.full_name} بنجاح.")
    else:
        messages.error(request, "قيمة المستوى غير صحيحة.")
    return redirect("affiliates:detail", pk=affiliate.pk)


@role_required("is_merchant")
@require_POST
def affiliate_edit_notes(request, pk):
    affiliate = get_owned_affiliate_or_404(request.user, pk)
    form = AffiliateNotesForm(request.POST, instance=affiliate)
    if form.is_valid():
        services.set_notes(affiliate, form.cleaned_data["notes"])
        messages.success(request, "تم حفظ الملاحظات.")
    else:
        messages.error(request, "حدث خطأ أثناء حفظ الملاحظات.")
    return redirect("affiliates:detail", pk=affiliate.pk)
