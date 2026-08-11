from rest_framework import serializers
from .models import WorkerCategory, Post


class WorkerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerCategory
        fields = ["id", "name", "icon", "order"]


class PostSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    is_video = serializers.ReadOnlyField()
    worker_name = serializers.CharField(source="worker.first_name", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "worker", "worker_name", "image", "video", "image_url", "video_url", "is_video", "caption", "created_at"]
        read_only_fields = ["worker"]
        extra_kwargs = {
            "image": {"write_only": True, "required": False},
            "video": {"write_only": True, "required": False},
        }

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_video_url(self, obj):
        request = self.context.get("request")
        if obj.video and request:
            return request.build_absolute_uri(obj.video.url)
        return None

    MAX_VIDEO_SIZE_MB = 50

    def validate(self, attrs):
        image = attrs.get("image")
        video = attrs.get("video")
        if not image and not video:
            raise serializers.ValidationError("Rasm yoki video yuklashingiz shart.")
        if image and video:
            raise serializers.ValidationError("Bitta postga faqat rasm YOKI video yuklang.")
        if video:
            allowed_ext = (".mp4", ".webm", ".mov")
            if not video.name.lower().endswith(allowed_ext):
                raise serializers.ValidationError("Video formati faqat MP4, WebM yoki MOV bo'lishi mumkin.")
            if video.size > self.MAX_VIDEO_SIZE_MB * 1024 * 1024:
                raise serializers.ValidationError(f"Video hajmi {self.MAX_VIDEO_SIZE_MB} MB dan oshmasligi kerak.")
        return attrs
