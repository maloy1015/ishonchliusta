from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import RegisterSerializer, ProfileUpdateSerializer, UserPublicSerializer
from workers.utils import distance_km


class RegisterAPIView(generics.CreateAPIView):
    """POST /api/v1/auth/register/ — yangi foydalanuvchi (mobil ilova orqali ro'yxatdan o'tish)."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserPublicSerializer(user, context={"request": request}).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Standart JWT login, lekin javobga foydalanuvchi ma'lumotlarini ham qo'shadi."""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserPublicSerializer(self.user, context={"request": self.context.get("request")}).data
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """POST /api/v1/auth/login/ — {"username": ..., "password": ...} -> access + refresh + user."""
    serializer_class = CustomTokenObtainPairSerializer


class MeAPIView(APIView):
    """GET/PATCH/DELETE /api/v1/accounts/me/ — o'z profili."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserPublicSerializer(request.user, context={"request": request}).data)

    def patch(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserPublicSerializer(request.user, context={"request": request}).data)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """GET /api/v1/accounts/<id>/ — boshqa foydalanuvchi profili."""
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        return ctx

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.dist = distance_km(request.user.latitude, request.user.longitude, obj.latitude, obj.longitude)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class UpdateLocationAPIView(APIView):
    """POST /api/v1/accounts/location/ — {"latitude":.., "longitude":.., "address": ".." (ixtiyoriy)}"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            lat = float(request.data.get("latitude"))
            lng = float(request.data.get("longitude"))
        except (TypeError, ValueError):
            return Response({"detail": "Noto'g'ri lat/lng"}, status=status.HTTP_400_BAD_REQUEST)

        address = (request.data.get("address") or "").strip()
        request.user.latitude = lat
        request.user.longitude = lng
        request.user.location_updated_at = timezone.now()
        update_fields = ["latitude", "longitude", "location_updated_at"]
        if address:
            request.user.address = address[:255]
            update_fields.append("address")
        request.user.save(update_fields=update_fields)
        return Response({"ok": True, "address": request.user.address})
