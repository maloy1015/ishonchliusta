from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.first_name", read_only=True)
    voice_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id", "conversation", "sender", "sender_name", "message_type",
            "text", "sticker_code", "voice_file", "voice_file_url", "created_at", "is_read",
        ]
        read_only_fields = ["conversation", "sender", "is_read"]
        extra_kwargs = {"voice_file": {"write_only": True}}

    def get_voice_file_url(self, obj):
        request = self.context.get("request")
        if obj.voice_file and request:
            return request.build_absolute_uri(obj.voice_file.url)
        return None

    def validate(self, attrs):
        msg_type = attrs.get("message_type", "text")
        if msg_type == "text" and not attrs.get("text"):
            raise serializers.ValidationError("Matn xabar bo'sh bo'lishi mumkin emas.")
        if msg_type in ("sticker", "gif") and not attrs.get("sticker_code"):
            raise serializers.ValidationError("Stiker tanlanmagan.")
        if msg_type == "voice" and not attrs.get("voice_file"):
            raise serializers.ValidationError("Ovozli fayl topilmadi.")
        return attrs


class ConversationSerializer(serializers.ModelSerializer):
    other_id = serializers.SerializerMethodField()
    other_name = serializers.SerializerMethodField()
    other_image = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "other_id", "other_name", "other_image", "last_message", "created_at"]

    def _other(self, obj):
        request = self.context.get("request")
        return obj.other(request.user)

    def get_other_id(self, obj):
        return self._other(obj).pk

    def get_other_name(self, obj):
        other = self._other(obj)
        return other.first_name or other.username

    def get_other_image(self, obj):
        other = self._other(obj)
        request = self.context.get("request")
        if other.profile_image and request:
            return request.build_absolute_uri(other.profile_image.url)
        return None

    def get_last_message(self, obj):
        last = obj.last_message
        if not last:
            return None
        return {"type": last.message_type, "text": last.text, "created_at": last.created_at.strftime("%H:%M")}
