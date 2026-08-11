from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import JobPost
from .forms import JobPostForm
from workers.models import WorkerCategory
from workers.utils import distance_km


@login_required
def job_list_view(request):
    """Ishchi uchun — ish e'lonlari ro'yxati, qidiruv, radius va lokatsiyaga qarab saralangan."""
    from django.db.models import Q
    from django.utils import timezone
    from payments.models import BoostOrder

    category_id = request.GET.get("category", "")
    query = request.GET.get("q", "").strip()
    radius = request.GET.get("radius", "").strip()
    jobs = JobPost.objects.filter(status="ochiq").select_related("employer", "category")

    if category_id:
        jobs = jobs.filter(category_id=category_id)
    elif not query and request.user.is_worker and request.user.category_id:
        category_id = str(request.user.category_id)
        jobs = jobs.filter(category_id=request.user.category_id)

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | Q(description__icontains=query) |
            Q(category__name__icontains=query) | Q(address__icontains=query)
        )

    jobs = list(jobs)
    me = request.user
    boosted_ids = set(BoostOrder.objects.filter(
        boost_type="job_post", status="tolangan", expires_at__gt=timezone.now()
    ).values_list("job_id", flat=True))

    for j in jobs:
        j.dist = distance_km(me.latitude, me.longitude, j.employer.latitude, j.employer.longitude)
        j.is_boosted = j.pk in boosted_ids

    if radius:
        try:
            radius_val = float(radius)
            jobs = [j for j in jobs if j.dist is not None and j.dist <= radius_val]
        except ValueError:
            pass

    jobs.sort(key=lambda j: (not j.is_boosted, j.dist is None, j.dist if j.dist is not None else 0))

    categories = WorkerCategory.objects.all()
    return render(request, "jobs/job_list.html", {
        "jobs": jobs, "categories": categories, "selected_category": category_id,
        "query": query, "radius": radius,
    })


@login_required
def job_create_view(request):
    if not request.user.is_employer:
        messages.error(request, "Faqat ish beruvchilar e'lon joylashi mumkin.")
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, "E'loningiz joylandi!")
            return redirect("jobs:my_jobs")
    else:
        form = JobPostForm()
    return render(request, "jobs/job_form.html", {"form": form})


@login_required
def my_jobs_view(request):
    jobs = request.user.job_posts.all()
    return render(request, "jobs/my_jobs.html", {"jobs": jobs})


@login_required
def job_toggle_status_view(request, pk):
    job = get_object_or_404(JobPost, pk=pk, employer=request.user)
    if request.method == "POST":
        job.status = "yopiq" if job.status == "ochiq" else "ochiq"
        job.save()
    return redirect("jobs:my_jobs")


@login_required
def job_delete_view(request, pk):
    job = get_object_or_404(JobPost, pk=pk, employer=request.user)
    if request.method == "POST":
        job.delete()
        messages.success(request, "E'lon o'chirildi.")
    return redirect("jobs:my_jobs")
