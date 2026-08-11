from django import forms
from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["stars", "comment"]
        widgets = {
            "stars": forms.Select(choices=[(i, f"{i} ★") for i in range(1, 6)], attrs={"class": "form-select"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Ish sifati haqida fikringiz (ixtiyoriy)"}),
        }
