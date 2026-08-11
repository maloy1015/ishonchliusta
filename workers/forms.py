from django import forms
from .models import Post, WorkerCategory


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "video", "caption"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "video": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "video/mp4,video/webm,video/quicktime"}),
            "caption": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ish haqida qisqacha izoh"}),
        }

    MAX_VIDEO_SIZE_MB = 50

    def clean(self):
        cleaned = super().clean()
        image = cleaned.get("image")
        video = cleaned.get("video")

        if not image and not video:
            raise forms.ValidationError("Rasm yoki video yuklashingiz shart.")
        if image and video:
            raise forms.ValidationError("Bitta postga faqat rasm YOKI video yuklang, ikkalasini emas.")

        if video:
            allowed_ext = (".mp4", ".webm", ".mov")
            if not video.name.lower().endswith(allowed_ext):
                raise forms.ValidationError("Video formati faqat MP4, WebM yoki MOV bo'lishi mumkin.")
            if video.size > self.MAX_VIDEO_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(f"Video hajmi {self.MAX_VIDEO_SIZE_MB} MB dan oshmasligi kerak.")

        return cleaned


class CategoryForm(forms.ModelForm):
    class Meta:
        model = WorkerCategory
        fields = ["name", "icon", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Kasb nomi"}),
            "icon": forms.TextInput(attrs={"class": "form-control", "placeholder": "🛠️"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }
