from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class CategoryMiniSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.CharField()


class UserPublicSerializer(serializers.ModelSerializer):
    """Boshqalar ko'radigan ochiq profil ma'lumotlari."""
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_icon = serializers.CharField(source="category.icon", read_only=True)
    average_rating = serializers.ReadOnlyField()
    ratings_count = serializers.ReadOnlyField()
    profile_image = serializers.SerializerMethodField()
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "role", "phone", "bio", "profile_image",
            "category", "category_name", "category_icon", "experience_years",
            "latitude", "longitude", "address", "average_rating", "ratings_count",
            "distance_km", "created_at",
        ]

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return None

    def get_distance_km(self, obj):
        return getattr(obj, "dist", None)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["username", "first_name", "phone", "email", "address", "role", "category", "experience_years", "password"]

    def validate_phone(self, value):
        value = value.strip().replace(" ", "")
        if not value.startswith("+998") or len(value) != 13 or not value[1:].isdigit():
            raise serializers.ValidationError("Telefon raqami +998 bilan boshlanib, jami 13 ta belgidan iborat bo'lishi kerak.")
        return value

    def validate(self, attrs):
        if attrs.get("role") == "ishchi" and not attrs.get("category"):
            raise serializers.ValidationError({"category": "Ishchi sifatida ro'yxatdan o'tish uchun kasbingizni tanlang."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "phone", "email", "bio", "profile_image", "category", "experience_years", "address"]

    def validate_phone(self, value):
        value = value.strip().replace(" ", "")
        if not value.startswith("+998") or len(value) != 13 or not value[1:].isdigit():
            raise serializers.ValidationError("Telefon raqami +998 bilan boshlanib, jami 13 ta belgidan iborat bo'lishi kerak.")
        return value
