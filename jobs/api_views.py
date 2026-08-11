from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import JobPost
from .serializers import JobPostSerializer
from workers.utils import distance_km


class JobListAPIView(APIView):
    """GET /api/v1/jobs/?q=&category=&radius= — ish e'lonlari (qidiruv, masofa bo'yicha saralangan)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        category_id = request.query_params.get("category", "")
        query = request.query_params.get("q", "").strip()
        radius = request.query_params.get("radius", "").strip()

        jobs = JobPost.objects.filter(status="ochiq").select_related("employer", "category")
        if category_id:
            jobs = jobs.filter(category_id=category_id)
        elif not query and request.user.is_worker and request.user.category_id:
            jobs = jobs.filter(category_id=request.user.category_id)

        if query:
            jobs = jobs.filter(
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(category__name__icontains=query) | Q(address__icontains=query)
            )

        jobs = list(jobs)
        me = request.user
        for j in jobs:
            j.dist = distance_km(me.latitude, me.longitude, j.employer.latitude, j.employer.longitude)

        if radius:
            try:
                radius_val = float(radius)
                jobs = [j for j in jobs if j.dist is not None and j.dist <= radius_val]
            except ValueError:
                pass

        jobs.sort(key=lambda j: (j.dist is None, j.dist if j.dist is not None else 0))
        serializer = JobPostSerializer(jobs, many=True, context={"request": request})
        return Response(serializer.data)


class JobCreateAPIView(generics.CreateAPIView):
    """POST /api/v1/jobs/yarat/ — yangi ish e'loni (faqat ish beruvchi)."""
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_employer:
            raise PermissionDenied("Faqat ish beruvchilar e'lon joylashi mumkin.")
        serializer.save(employer=self.request.user)


class MyJobsAPIView(generics.ListAPIView):
    """GET /api/v1/jobs/mening-elonlarim/ — ish beruvchining o'z e'lonlari."""
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)


class JobToggleStatusAPIView(APIView):
    """PATCH /api/v1/jobs/<id>/holat/ — ochiq/yopiq holatini almashtirish."""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        job = get_object_or_404(JobPost, pk=pk, employer=request.user)
        job.status = "yopiq" if job.status == "ochiq" else "ochiq"
        job.save()
        return Response(JobPostSerializer(job, context={"request": request}).data)


class JobDeleteAPIView(generics.DestroyAPIView):
    """DELETE /api/v1/jobs/<id>/ — faqat o'z e'lonini o'chiradi."""
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)
