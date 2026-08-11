from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class BoostOrder(models.Model):
    """
    'Tezkor xizmat' uchun to'lov buyurtmasi.
    - Ishchi uchun: 'Tezkor ish topish' — o'z profilini 24 soat ustalar ro'yxati boshida ko'rsatadi.
    - Ish beruvchi uchun: 'Tezkor buyurtma' — bitta ish e'lonini 24 soat ish e'lonlari boshida ko'rsatadi.
    """
    TYPE_CHOICES = [
        ("worker_profile", "Tezkor ish topish (usta profili)"),
        ("job_post", "Tezkor buyurtma (ish e'loni)"),
    ]
    STATUS_CHOICES = [
        ("kutilmoqda", "To'lov kutilmoqda"),
        ("tolangan", "To'langan"),
        ("bekor_qilingan", "Bekor qilingan"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="boost_orders", verbose_name="Foydalanuvchi"
    )
    boost_type = models.CharField("Turi", max_length=20, choices=TYPE_CHOICES)
    job = models.ForeignKey(
        "jobs.JobPost", on_delete=models.CASCADE, null=True, blank=True,
        related_name="boost_orders", verbose_name="Ish e'loni (agar job_post bo'lsa)"
    )

    amount = models.PositiveIntegerField("Summasi (tiyin, ya'ni so'm x 100)")
    status = models.CharField("Holati", max_length=20, choices=STATUS_CHOICES, default="kutilmoqda")

    payme_transaction_id = models.CharField("Payme tranzaksiya ID", max_length=64, blank=True, db_index=True)
    payme_state = models.IntegerField("Payme holati (1=yaratildi,2=amalga oshdi,-1/-2=bekor)", null=True, blank=True)
    payme_create_time = models.BigIntegerField("Payme create_time (ms)", null=True, blank=True)
    payme_perform_time = models.BigIntegerField("Payme perform_time (ms)", null=True, blank=True)
    payme_cancel_time = models.BigIntegerField("Payme cancel_time (ms)", null=True, blank=True)
    payme_reason = models.IntegerField("Bekor qilish sababi (Payme kodi)", null=True, blank=True)

    created_at = models.DateTimeField("Yaratilgan sana", auto_now_add=True)
    expires_at = models.DateTimeField("Boost tugash vaqti", null=True, blank=True)

    class Meta:
        verbose_name = "Tezkor xizmat buyurtmasi"
        verbose_name_plural = "Tezkor xizmat buyurtmalari"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} — {self.user} — {self.get_boost_type_display()} — {self.get_status_display()}"

    @property
    def amount_som(self):
        return self.amount // 100

    def activate(self):
        """To'lov muvaffaqiyatli amalga oshganda chaqiriladi — 24 soatlik boostni faollashtiradi."""
        self.status = "tolangan"
        self.expires_at = timezone.now() + timedelta(hours=24)
        self.save(update_fields=["status", "expires_at"])

    @property
    def is_active(self):
        return self.status == "tolangan" and self.expires_at and self.expires_at > timezone.now()
