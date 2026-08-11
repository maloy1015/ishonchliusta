from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404

from .models import Rating
from .serializers import RatingSerializer
from accounts.models import User


class RateWorkerAPIView(generics.CreateAPIView):
    """POST /api/v1/ratings/<worker_id>/ — {"stars": 1-5, "comment": "..."} (faqat ish beruvchi)."""
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        worker = get_object_or_404(User, pk=self.kwargs["worker_id"], role="ishchi")
        if not self.request.user.is_employer:
            raise PermissionDenied("Faqat ish beruvchilar baho qo'ya oladi.")
        serializer.save(employer=self.request.user, worker=worker)


class LeaderboardAPIView(generics.ListAPIView):
    """GET /api/v1/ratings/reyting/?category= — eng yuqori baholangan ustalar."""
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        category_id = self.request.query_params.get("category", "")
        workers = User.objects.filter(role="ishchi").annotate(
            avg_rating=Avg("received_ratings__stars"),
            ratings_total=Count("received_ratings"),
        ).filter(ratings_total__gt=0)
        if category_id:
            workers = workers.filter(category_id=category_id)
        return workers.order_by("-avg_rating", "-ratings_total")

    def list(self, request, *args, **kwargs):
        workers = self.get_queryset()
        data = [{
            "id": w.pk, "first_name": w.first_name or w.username,
            "category_name": w.category.name if w.category else None,
            "category_icon": w.category.icon if w.category else None,
            "avg_rating": round(w.avg_rating, 1), "ratings_total": w.ratings_total,
        } for w in workers]
        return Response(data)
