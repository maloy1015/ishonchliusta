from django.db import models
from django.conf import settings


class WorkerCategory(models.Model):
    """Ishchi kasb turi: santexnik, elektrik, suvoqchi va h.k."""
    name = models.CharField("Nomi", max_length=100, unique=True)
    icon = models.CharField("Ikonka (emoji)", max_length=10, blank=True, default="🛠️")
    order = models.PositiveIntegerField("Tartib raqami", default=0)

    class Meta:
        verbose_name = "Kasb kategoriyasi"
        verbose_name_plural = "Kasb kategoriyalari"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    """Ishchining portfolio posti — bajargan ishlari rasmi yoki videosi."""
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts", verbose_name="Ishchi"
    )
    image = models.ImageField("Rasm", upload_to="posts/images/", blank=True, null=True)
    video = models.FileField("Video", upload_to="posts/videos/", blank=True, null=True)
    caption = models.CharField("Izoh", max_length=255, blank=True)
    created_at = models.DateTimeField("Joylangan sana", auto_now_add=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.worker} — post #{self.pk}"

    @property
    def is_video(self):
        return bool(self.video)
