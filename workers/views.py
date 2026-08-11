from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import WorkerCategory, Post
from .forms import PostForm
from .utils import distance_km
from accounts.models import User


@login_required
def worker_list_view(request):
    """Ish beruvchi uchun — ustalar ro'yxati, ism/kasb bo'yicha qidiruv, radius va lokatsiyaga yaqinlik bo'yicha saralash."""
    from django.db.models import Q
    from django.utils import timezone
    from payments.models import BoostOrder

    category_id = request.GET.get("category")
    query = request.GET.get("q", "").strip()
    radius = request.GET.get("radius", "").strip()
    workers = User.objects.filter(role="ishchi").select_related("category")

    if category_id:
        workers = workers.filter(category_id=category_id)
    if query:
        workers = workers.filter(
            Q(first_name__icontains=query) | Q(username__icontains=query) |
            Q(category__name__icontains=query) | Q(bio__icontains=query)
        )

    workers = list(workers)
    me = request.user
    boosted_ids = set(BoostOrder.objects.filter(
        boost_type="worker_profile", status="tolangan", expires_at__gt=timezone.now()
    ).values_list("user_id", flat=True))

    for w in workers:
        w.dist = distance_km(me.latitude, me.longitude, w.latitude, w.longitude)
        w.is_boosted = w.pk in boosted_ids

    if radius:
        try:
            radius_val = float(radius)
            workers = [w for w in workers if w.dist is not None and w.dist <= radius_val]
        except ValueError:
            pass

    workers.sort(key=lambda w: (not w.is_boosted, w.dist is None, w.dist if w.dist is not None else 0))

    categories = WorkerCategory.objects.all()
    return render(request, "workers/worker_list.html", {
        "workers": workers, "categories": categories, "selected_category": category_id,
        "query": query, "radius": radius,
    })


@login_required
def post_create_view(request):
    if not request.user.is_worker:
        messages.error(request, "Faqat ishchilar post joylashi mumkin.")
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.worker = request.user
            post.save()
            messages.success(request, "Postingiz joylandi!")
            return redirect("accounts:profile_detail", pk=request.user.pk)
    else:
        form = PostForm()
    return render(request, "workers/post_form.html", {"form": form})


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk, worker=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post o'chirildi.")
    return redirect("accounts:profile_detail", pk=request.user.pk)
