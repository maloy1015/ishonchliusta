from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqami +998 bilan boshlanib, jami 13 ta belgidan iborat bo'lishi kerak. Masalan: +998901234567"
)


class User(AbstractUser):
    ROLE_CHOICES = [
        ("ishchi", "Ishchi (Usta)"),
        ("ish_beruvchi", "Ish beruvchi"),
    ]

    role = models.CharField("Roli", max_length=20, choices=ROLE_CHOICES, default="ish_beruvchi")
    phone = models.CharField(
        "Telefon raqami", max_length=13, validators=[phone_validator],
        unique=True, null=True, blank=True
    )
    profile_image = models.ImageField("Profil rasmi", upload_to="profiles/", blank=True, null=True)
    bio = models.TextField("O'zi haqida", blank=True)

    category = models.ForeignKey(
        "workers.WorkerCategory", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="workers", verbose_name="Kasb kategoriyasi"
    )
    experience_years = models.PositiveIntegerField("Tajriba (yil)", null=True, blank=True)

    latitude = models.FloatField("Kenglik (lat)", null=True, blank=True)
    longitude = models.FloatField("Uzunlik (lng)", null=True, blank=True)
    address = models.CharField("Manzil (matn ko'rinishida)", max_length=255, blank=True)
    location_updated_at = models.DateTimeField("Lokatsiya yangilangan vaqti", null=True, blank=True)

    created_at = models.DateTimeField("Ro'yxatdan o'tgan sana", auto_now_add=True)

    def __str__(self):
        full = self.get_full_name()
        return full if full else self.username

    @property
    def is_worker(self):
        return self.role == "ishchi"

    @property
    def is_employer(self):
        return self.role == "ish_beruvchi"

    @property
    def average_rating(self):
        agg = self.received_ratings.aggregate(avg=models.Avg("stars"))
        return round(agg["avg"], 1) if agg["avg"] else None

    @property
    def ratings_count(self):
        return self.received_ratings.count()
