from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Conversation, Message
from accounts.models import User


@login_required
def inbox_view(request):
    conversations = Conversation.objects.filter(
        Q(participant1=request.user) | Q(participant2=request.user)
    ).order_by("-created_at")
    rows = []
    for c in conversations:
        rows.append({"conversation": c, "other": c.other(request.user), "last": c.last_message})
    rows.sort(key=lambda r: r["last"].created_at if r["last"] else r["conversation"].created_at, reverse=True)
    return render(request, "chat/inbox.html", {"rows": rows})


@login_required
def start_conversation_view(request, user_id):
    other = get_object_or_404(User, pk=user_id)
    if other.pk == request.user.pk:
        messages.error(request, "O'zingiz bilan chat ochib bo'lmaydi.")
        return redirect("accounts:dashboard")
    convo = Conversation.get_or_create_between(request.user, other)
    return redirect("chat:conversation", pk=convo.pk)


@login_required
def conversation_view(request, pk):
    convo = get_object_or_404(
        Conversation.objects.filter(Q(participant1=request.user) | Q(participant2=request.user)), pk=pk
    )
    convo.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    other = convo.other(request.user)

    STICKERS = ["👍", "🙏", "😂", "❤️", "🔥", "👏", "🤝", "✅", "😢", "😍", "🎉", "💪"]
    GIFS = ["🕺", "🎊", "🤩", "🙌", "🥳", "👌"]  # oddiy animatsion-hissiy stikerlar (demo GIF o'rnida)

    return render(request, "chat/conversation.html", {
        "conversation": convo, "other": other, "messages_list": convo.messages.select_related("sender").all(),
        "stickers": STICKERS, "gifs": GIFS,
    })


@login_required
@require_POST
def send_message_view(request, pk):
    convo = get_object_or_404(
        Conversation.objects.filter(Q(participant1=request.user) | Q(participant2=request.user)), pk=pk
    )
    msg_type = request.POST.get("message_type", "text")
    message = Message(conversation=convo, sender=request.user, message_type=msg_type)

    if msg_type == "text":
        text = request.POST.get("text", "").strip()
        if not text:
            return JsonResponse({"ok": False, "error": "Bo'sh xabar"}, status=400)
        message.text = text
    elif msg_type in ("sticker", "gif"):
        message.sticker_code = request.POST.get("sticker_code", "")
        if not message.sticker_code:
            return JsonResponse({"ok": False, "error": "Stiker tanlanmagan"}, status=400)
    elif msg_type == "voice":
        audio = request.FILES.get("voice_file")
        if not audio:
            return JsonResponse({"ok": False, "error": "Ovozli fayl topilmadi"}, status=400)
        message.voice_file = audio
    else:
        return JsonResponse({"ok": False, "error": "Noto'g'ri xabar turi"}, status=400)

    message.save()
    return JsonResponse({
        "ok": True,
        "message": {
            "id": message.pk,
            "type": message.message_type,
            "text": message.text,
            "sticker_code": message.sticker_code,
            "voice_url": message.voice_file.url if message.voice_file else None,
            "sender_id": message.sender_id,
            "sender_name": message.sender.first_name or message.sender.username,
            "created_at": message.created_at.strftime("%H:%M"),
        }
    })


@login_required
def live_location_page_view(request, pk):
    convo = get_object_or_404(
        Conversation.objects.filter(Q(participant1=request.user) | Q(participant2=request.user)), pk=pk
    )
    other = convo.other(request.user)
    return render(request, "chat/live_location.html", {"conversation": convo, "other": other})


@login_required
def live_locations_data_view(request, pk):
    """Ikki foydalanuvchining joriy lokatsiyasini JSON qilib qaytaradi (xaritani jonli yangilash uchun)."""
    convo = get_object_or_404(
        Conversation.objects.filter(Q(participant1=request.user) | Q(participant2=request.user)), pk=pk
    )
    other = convo.other(request.user)
    me = request.user

    def serialize(u):
        return {
            "id": u.pk,
            "name": u.first_name or u.username,
            "lat": u.latitude,
            "lng": u.longitude,
            "updated_at": u.location_updated_at.strftime("%H:%M:%S") if u.location_updated_at else None,
        }

    return JsonResponse({"me": serialize(me), "other": serialize(other)})


@login_required
def fetch_messages_view(request, pk):
    convo = get_object_or_404(
        Conversation.objects.filter(Q(participant1=request.user) | Q(participant2=request.user)), pk=pk
    )
    after_id = int(request.GET.get("after", 0))
    qs = convo.messages.filter(pk__gt=after_id).select_related("sender")
    qs.exclude(sender=request.user).update(is_read=True)
    data = [{
        "id": m.pk, "type": m.message_type, "text": m.text, "sticker_code": m.sticker_code,
        "voice_url": m.voice_file.url if m.voice_file else None,
        "sender_id": m.sender_id, "sender_name": m.sender.first_name or m.sender.username,
        "created_at": m.created_at.strftime("%H:%M"),
    } for m in qs]
    return JsonResponse({"messages": data})
