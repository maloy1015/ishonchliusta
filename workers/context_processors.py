from .models import WorkerCategory


def categories(request):
    """Barcha shablonlarga kategoriyalar ro'yxatini beradi (navbar'dagi 'Kategoriyalar' oynasi uchun)."""
    if not request.user.is_authenticated:
        return {}
    return {"nav_categories": WorkerCategory.objects.all()}
