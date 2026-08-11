from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse

from .models import BoostOrder
from .utils import build_payme_checkout_url
from jobs.models import JobPost


@login_required
def boost_worker_profile_view(request):
    """Ishchi — 'Tezkor ish topish': o'z profilini 24 soatga ustalar ro'yxati boshiga chiqaradi."""
    if not request.user.is_worker:
        messages.error(request, "Bu xizmat faqat ishchilar uchun.")
        return redirect("accounts:dashboard")

    existing = BoostOrder.objects.filter(
        user=request.user, boost_type="worker_profile", status="tolangan"
    ).order_by("-expires_at").first()
    active_boost = existing if (existing and existing.is_active) else None

    if request.method == "POST" and not active_boost:
        order = BoostOrder.objects.create(
            user=request.user, boost_type="worker_profile",
            amount=settings.PAYME_BOOST_PRICE_SOM * 100,
        )
        return redirect("payments:checkout", order_id=order.pk)

    return render(request, "payments/boost_worker.html", {
        "price_som": settings.PAYME_BOOST_PRICE_SOM, "active_boost": active_boost,
    })


@login_required
def boost_job_view(request, job_id):
    """Ish beruvchi — 'Tezkor buyurtma': bitta ish e'lonini 24 soatga ro'yxat boshiga chiqaradi."""
    job = get_object_or_404(JobPost, pk=job_id, employer=request.user)

    existing = BoostOrder.objects.filter(
        job=job, boost_type="job_post", status="tolangan"
    ).order_by("-expires_at").first()
    active_boost = existing if (existing and existing.is_active) else None

    if request.method == "POST" and not active_boost:
        order = BoostOrder.objects.create(
            user=request.user, boost_type="job_post", job=job,
            amount=settings.PAYME_BOOST_PRICE_SOM * 100,
        )
        return redirect("payments:checkout", order_id=order.pk)

    return render(request, "payments/boost_job.html", {
        "job": job, "price_som": settings.PAYME_BOOST_PRICE_SOM, "active_boost": active_boost,
    })


@login_required
def checkout_view(request, order_id):
    """Payme to'lov sahifasiga yo'naltiruvchi oraliq sahifa."""
    order = get_object_or_404(BoostOrder, pk=order_id, user=request.user)

    if order.status == "tolangan":
        return redirect("payments:return_page", order_id=order.pk)

    return_url = request.build_absolute_uri(reverse("payments:return_page", args=[order.pk]))
    checkout_url = build_payme_checkout_url(order.pk, order.amount, return_url=return_url)

    return render(request, "payments/checkout.html", {
        "order": order, "checkout_url": checkout_url,
    })


@login_required
def return_page_view(request, order_id):
    """Payme to'lovdan keyin foydalanuvchini shu sahifaga qaytaradi."""
    order = get_object_or_404(BoostOrder, pk=order_id, user=request.user)
    return render(request, "payments/return_page.html", {"order": order})
