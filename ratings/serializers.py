from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source="employer.first_name", read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "employer", "employer_name", "worker", "stars", "comment", "created_at"]
        read_only_fields = ["employer", "worker"]


class LeaderboardWorkerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    username = serializers.CharField()
    category_name = serializers.CharField(source="category.name", allow_null=True)
    category_icon = serializers.CharField(source="category.icon", allow_null=True)
    avg_rating = serializers.FloatField()
    ratings_total = serializers.IntegerField()
