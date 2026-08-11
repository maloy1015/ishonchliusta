from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from workers.models import WorkerCategory


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Ismingiz", max_length=150, required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ismingizni kiriting"})
    )
    phone = forms.CharField(
        label="Telefon raqami", max_length=13, required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control", "placeholder": "+998901234567",
            "pattern": r"\+998\d{9}", "title": "Masalan: +998901234567"
        })
    )
    role = forms.ChoiceField(
        label="Siz kimsiz?", choices=User.ROLE_CHOICES, required=True,
        widget=forms.RadioSelect(attrs={"class": "role-radio"})
    )
    category = forms.ModelChoiceField(
        label="Kasbingiz (qanday usta ekanligingiz)", queryset=WorkerCategory.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    experience_years = forms.IntegerField(
        label="Tajribangiz (necha yil)", required=False, min_value=0, max_value=60,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Masalan: 5"})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "phone", "role", "category", "experience_years", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Login"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Parol"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Parolni takrorlang"})

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip().replace(" ", "")
        if not phone.startswith("+998") or len(phone) != 13 or not phone[1:].isdigit():
            raise forms.ValidationError("Telefon raqami +998 bilan boshlanib, jami 13 ta belgidan iborat bo'lishi kerak.")
        return phone

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("role") == "ishchi" and not cleaned.get("category"):
            self.add_error("category", "Ishchi sifatida ro'yxatdan o'tish uchun kasbingizni tanlang.")
        return cleaned


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "phone", "bio", "profile_image", "category", "experience_years"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "pattern": r"\+998\d{9}"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "O'zingiz haqingizda qisqacha..."}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "experience_years": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip().replace(" ", "")
        if not phone.startswith("+998") or len(phone) != 13 or not phone[1:].isdigit():
            raise forms.ValidationError("Telefon raqami +998 bilan boshlanib, jami 13 ta belgidan iborat bo'lishi kerak.")
        return phone
