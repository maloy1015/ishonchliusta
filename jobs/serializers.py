from rest_framework import serializers
from .models import JobPost


class JobPostSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source="employer.first_name", read_only=True)
    employer_phone = serializers.CharField(source="employer.phone", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_icon = serializers.CharField(source="category.icon", read_only=True)
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = JobPost
        fields = [
            "id", "employer", "employer_name", "employer_phone", "category", "category_name", "category_icon",
            "title", "description", "budget", "address", "status", "distance_km", "created_at",
        ]
        read_only_fields = ["employer", "status"]

    def get_distance_km(self, obj):
        return getattr(obj, "dist", None)
