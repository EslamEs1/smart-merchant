from django.shortcuts import render

from apps.core.decorators import role_required


@role_required("is_merchant")
def merchant_dashboard(request):
    return render(request, "dashboard.html")


@role_required("is_affiliate")
def affiliate_dashboard(request):
    return render(request, "affiliate-dashboard.html")
