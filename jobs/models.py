from django.db import models
from django.conf import settings
from workers.models import WorkerCategory


class JobPost(models.Model):
    STATUS_CHOICES = [
        ("ochiq", "Ochiq"),
        ("yopiq", "Yopiq"),
    ]

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_posts", verbose_name="Ish beruvchi"
    )
    category = models.ForeignKey(
        WorkerCategory, on_delete=models.SET_NULL, null=True, related_name="job_posts", verbose_name="Kategoriya"
    )
    title = models.CharField("Sarlavha", max_length=200)
    description = models.TextField("Tavsif")
    budget = models.DecimalField("Byudjet (so'm)", max_digits=12, decimal_places=0, null=True, blank=True)
    address = models.CharField("Manzil", max_length=255, blank=True)
    status = models.CharField("Holati", max_length=10, choices=STATUS_CHOICES, default="ochiq")
    created_at = models.DateTimeField("E'lon qilingan sana", auto_now_add=True)

    class Meta:
        verbose_name = "Ish e'loni"
        verbose_name_plural = "Ish e'lonlari"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
