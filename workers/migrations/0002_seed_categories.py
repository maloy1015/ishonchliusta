from django.db import migrations

CATEGORIES = [
    ("Santexnik", "🚿", 1),
    ("Elektrik", "💡", 2),
    ("Suvoqchi", "🧱", 3),
    ("G'isht teruvchi", "🧱", 4),
    ("Bo'yoqchi", "🎨", 5),
    ("Plitka teruvchi", "🔲", 6),
    ("Konditsioner ustasi", "❄️", 7),
    ("Duradgor (yog'ochchi)", "🪚", 8),
    ("Payvandchi", "🔥", 9),
    ("Mebel yig'uvchi", "🛋️", 10),
    ("Tomchi (tom ustasi)", "🏠", 11),
    ("Muzlatgich ustasi", "🧊", 12),
    ("Kir yuvish mashinasi ustasi", "🌀", 13),
    ("Kompyuter ustasi", "💻", 14),
    ("Telefon ustasi", "📱", 15),
    ("Avtomexanik", "🚗", 16),
    ("Haydovchi", "🚕", 17),
    ("Tozalovchi", "🧹", 18),
    ("Bog'bon", "🌳", 19),
    ("Dizayner (interyer)", "📐", 20),
    ("Tikuvchi", "🧵", 21),
    ("Oshpaz", "👨‍🍳", 22),
    ("Ustoz/repetitor", "📚", 23),
    ("Boshqa xizmatlar", "🛠️", 99),
]


def seed_categories(apps, schema_editor):
    WorkerCategory = apps.get_model("workers", "WorkerCategory")
    for name, icon, order in CATEGORIES:
        WorkerCategory.objects.get_or_create(name=name, defaults={"icon": icon, "order": order})


def remove_categories(apps, schema_editor):
    WorkerCategory = apps.get_model("workers", "WorkerCategory")
    WorkerCategory.objects.filter(name__in=[c[0] for c in CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("workers", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, remove_categories),
    ]
