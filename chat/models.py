from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Ikki foydalanuvchi (ishchi va ish beruvchi) o'rtasidagi suhbat."""
    participant1 = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations_as_p1"
    )
    participant2 = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations_as_p2"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("participant1", "participant2")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.participant1} ↔ {self.participant2}"

    def other(self, user):
        return self.participant2 if self.participant1_id == user.id else self.participant1

    @property
    def last_message(self):
        return self.messages.order_by("-created_at").first()

    @staticmethod
    def get_or_create_between(user_a, user_b):
        convo = Conversation.objects.filter(
            models.Q(participant1=user_a, participant2=user_b) |
            models.Q(participant1=user_b, participant2=user_a)
        ).first()
        if convo:
            return convo
        return Conversation.objects.create(participant1=user_a, participant2=user_b)


class Message(models.Model):
    TYPE_CHOICES = [
        ("text", "Matn"),
        ("sticker", "Stiker"),
        ("gif", "GIF"),
        ("voice", "Ovozli xabar"),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    message_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="text")
    text = models.TextField(blank=True)
    sticker_code = models.CharField(max_length=20, blank=True)
    voice_file = models.FileField(upload_to="voice_messages/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender} [{self.message_type}] {self.created_at:%H:%M}"
