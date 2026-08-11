import json
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone

from .forms import RegisterForm, ProfileEditForm
from .models import User
from workers.utils import distance_km
from jobs.models import JobPost


def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data["role"]
            if user.role == "ish_beruvchi":
                user.category = None
                user.experience_years = None
            user.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz! Xush kelibsiz.")
            return redirect("accounts:dashboard")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard_view(request):
    """Kirgandan keyingi bosh sahifa — rolga qarab boshqacha ko'rinish."""
    if request.user.is_worker:
        recent_jobs = JobPost.objects.filter(status="ochiq").select_related("employer", "category").order_by("-created_at")[:4]
        return render(request, "accounts/home_worker.html", {
            "recent_jobs": recent_jobs,
        })

    top_workers = User.objects.filter(role="ishchi").select_related("category").order_by("-created_at")[:6]
    return render(request, "accounts/home_employer.html", {
        "top_workers": top_workers,
    })


@login_required
def profile_edit_view(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilingiz yangilandi.")
            return redirect("accounts:profile_detail", pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "accounts/profile_edit.html", {"form": form})


@login_required
def profile_detail_view(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    posts = profile_user.posts.all() if profile_user.is_worker else None
    ratings = profile_user.received_ratings.select_related("employer").all()[:10] if profile_user.is_worker else None
    dist = None
    if request.user.latitude and profile_user.latitude:
        dist = distance_km(request.user.latitude, request.user.longitude, profile_user.latitude, profile_user.longitude)
    return render(request, "accounts/profile_detail.html", {
        "profile_user": profile_user, "posts": posts, "ratings": ratings, "distance": dist,
    })


@login_required
def delete_account_view(request):
    if request.method == "POST":
        user = request.user
        from django.contrib.auth import logout
        logout(request)
        user.delete()
        messages.success(request, "Hisobingiz butunlay o'chirildi.")
        return redirect("accounts:login")
    return render(request, "accounts/delete_account.html")


@login_required
def location_picker_view(request):
    """Xaritadan qo'lda lokatsiya tanlash yoki manzil bo'yicha qidirish sahifasi."""
    return render(request, "accounts/location_picker.html")


@login_required
@require_POST
def update_location_view(request):
    """Brauzerdan JS orqali (GPS yoki xaritadan qo'lda tanlangan) lokatsiyani saqlaydi (AJAX)."""
    try:
        data = json.loads(request.body)
        lat = float(data.get("latitude"))
        lng = float(data.get("longitude"))
    except (TypeError, ValueError, json.JSONDecodeError):
        return JsonResponse({"ok": False, "error": "Noto'g'ri ma'lumot"}, status=400)

    address = (data.get("address") or "").strip()

    request.user.latitude = lat
    request.user.longitude = lng
    request.user.location_updated_at = timezone.now()
    update_fields = ["latitude", "longitude", "location_updated_at"]
    if address:
        request.user.address = address[:255]
        update_fields.append("address")
    request.user.save(update_fields=update_fields)
    return JsonResponse({"ok": True, "address": request.user.address})
