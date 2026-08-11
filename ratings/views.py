from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count

from .models import Rating
from .forms import RatingForm
from accounts.models import User
from workers.models import WorkerCategory


@login_required
def rate_worker_view(request, pk):
    worker = get_object_or_404(User, pk=pk, role="ishchi")
    if not request.user.is_employer:
        messages.error(request, "Faqat ish beruvchilar baho qo'ya oladi.")
        return redirect("accounts:profile_detail", pk=pk)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.employer = request.user
            rating.worker = worker
            rating.save()
            messages.success(request, f"{worker} uchun bahoyingiz qabul qilindi. Rahmat!")
            return redirect("accounts:profile_detail", pk=pk)
    else:
        form = RatingForm()
    return render(request, "ratings/rate_form.html", {"form": form, "worker": worker})


@login_required
def leaderboard_view(request):
    """Eng yuqori baholangan ustalar reytingi (ish beruvchi paneli uchun)."""
    category_id = request.GET.get("category", "")
    workers = User.objects.filter(role="ishchi").annotate(
        avg_rating=Avg("received_ratings__stars"),
        ratings_total=Count("received_ratings"),
    ).filter(ratings_total__gt=0)

    if category_id:
        workers = workers.filter(category_id=category_id)

    workers = workers.order_by("-avg_rating", "-ratings_total")
    categories = WorkerCategory.objects.all()
    return render(request, "ratings/leaderboard.html", {
        "workers": workers, "categories": categories, "selected_category": category_id,
    })
