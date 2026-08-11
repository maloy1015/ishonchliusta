from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from accounts.models import User


class ConversationListAPIView(generics.ListAPIView):
    """GET /api/v1/chat/conversations/ — suhbatlar ro'yxati (so'nggi xabar bilan)."""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Conversation.objects.filter(
            Q(participant1=self.request.user) | Q(participant2=self.request.user)
        )


class StartConversationAPIView(APIView):
    """POST /api/v1/chat/boshlash/<user_id>/ — suhbat topadi yoki yaratadi."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        other = get_object_or_404(User, pk=user_id)
        if other.pk == request.user.pk:
            return Response({"detail": "O'zingiz bilan chat ochib bo'lmaydi."}, status=status.HTTP_400_BAD_REQUEST)
        convo = Conversation.get_or_create_between(request.user, other)
        return Response(ConversationSerializer(convo, context={"request": request}).data)


class MessageListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /api/v1/chat/conversations/<id>/messages/?after=<id> — xabarlar (polling uchun ?after=)
    POST /api/v1/chat/conversations/<id>/messages/ — xabar yuborish (text/sticker/gif/voice)
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_conversation(self):
        return get_object_or_404(
            Conversation.objects.filter(Q(participant1=self.request.user) | Q(participant2=self.request.user)),
            pk=self.kwargs["pk"]
        )

    def get_queryset(self):
        convo = self.get_conversation()
        qs = convo.messages.select_related("sender")
        after = self.request.query_params.get("after")
        if after:
            qs = qs.filter(pk__gt=after)
        qs.exclude(sender=self.request.user).filter(is_read=False).update(is_read=True)
        return qs

    def perform_create(self, serializer):
        convo = self.get_conversation()
        serializer.save(conversation=convo, sender=self.request.user)


class LiveLocationAPIView(APIView):
    """GET /api/v1/chat/conversations/<id>/jonli-lokatsiya/ — ikkala tomonning joriy lokatsiyasi."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        convo = get_object_or_404(
            Conversation.objects.filter(Q(participant1=request.user) | Q(participant2=request.user)), pk=pk
        )
        other = convo.other(request.user)
        me = request.user

        def serialize(u):
            return {
                "id": u.pk, "name": u.first_name or u.username,
                "lat": u.latitude, "lng": u.longitude,
                "updated_at": u.location_updated_at.strftime("%H:%M:%S") if u.location_updated_at else None,
            }

        return Response({"me": serialize(me), "other": serialize(other)})
