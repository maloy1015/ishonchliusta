from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import WorkerCategory, Post
from .serializers import WorkerCategorySerializer, PostSerializer
from .utils import distance_km
from accounts.models import User
from accounts.serializers import UserPublicSerializer


class CategoryListAPIView(generics.ListAPIView):
    """GET /api/v1/categories/ — barcha kasb kategoriyalari."""
    queryset = WorkerCategory.objects.all()
    serializer_class = WorkerCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class WorkerListAPIView(APIView):
    """GET /api/v1/workers/?q=&category=&radius= — ustalar ro'yxati (qidiruv, filtr, masofa bo'yicha saralangan)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        category_id = request.query_params.get("category")
        query = request.query_params.get("q", "").strip()
        radius = request.query_params.get("radius", "").strip()

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
        for w in workers:
            w.dist = distance_km(me.latitude, me.longitude, w.latitude, w.longitude)

        if radius:
            try:
                radius_val = float(radius)
                workers = [w for w in workers if w.dist is not None and w.dist <= radius_val]
            except ValueError:
                pass

        workers.sort(key=lambda w: (w.dist is None, w.dist if w.dist is not None else 0))
        serializer = UserPublicSerializer(workers, many=True, context={"request": request})
        return Response(serializer.data)


class PostListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /api/v1/workers/<worker_id>/posts/ — bitta ishchining postlari
    POST /api/v1/workers/posts/ — yangi post qo'shish (faqat ishchi, o'zi uchun)
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        worker_id = self.kwargs.get("worker_id")
        if worker_id:
            return Post.objects.filter(worker_id=worker_id)
        return Post.objects.filter(worker=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_worker:
            raise PermissionDenied("Faqat ishchilar post joylashi mumkin.")
        serializer.save(worker=self.request.user)


class PostDeleteAPIView(generics.DestroyAPIView):
    """DELETE /api/v1/workers/posts/<id>/ — faqat o'z postini o'chiradi."""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(worker=self.request.user)
