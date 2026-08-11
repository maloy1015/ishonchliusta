from django import forms
from .models import JobPost


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ["category", "title", "description", "budget", "address"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Masalan: Vannaxona kranini almashtirish"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Ish haqida batafsil yozing"}),
            "budget": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Taxminiy byudjet (so'm)"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Manzil"}),
        }
