from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    """Ish beruvchi tomonidan ishchiga qo'yiladigan baho."""
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="given_ratings", verbose_name="Baholovchi"
    )
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_ratings", verbose_name="Ishchi"
    )
    stars = models.PositiveSmallIntegerField("Yulduzchalar", validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField("Izoh", blank=True)
    created_at = models.DateTimeField("Sana", auto_now_add=True)

    class Meta:
        verbose_name = "Baho"
        verbose_name_plural = "Baholar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.worker} — {self.stars}★ ({self.employer})"
