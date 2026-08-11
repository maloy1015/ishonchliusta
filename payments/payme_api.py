"""
Payme Merchant API (JSON-RPC 2.0) — Payme serveri to'lovni tasdiqlash uchun shu endpointga
so'rov yuboradi: CheckPerformTransaction -> CreateTransaction -> PerformTransaction
(yoki xato bo'lsa CancelTransaction). Hujjat: https://developer.help.paycom.uz/

Bu yerga Payme haqiqiy pul o'tkazishdan OLDIN va KEYIN so'rov yuboradi — shuning uchun bu
sahifa ochiq (login talab qilinmaydi), lekin har bir so'rov Basic Auth orqali
(login: Paycom, parol: PAYME_MERCHANT_KEY) tekshiriladi.

MUHIM: Payme bu manzilga faqat sizning saytingiz ochiq internetda (HTTPS) turgan bo'lsagina
murojaat qila oladi — localhost'da ishlamaydi. Business.payme.uz panelida shu endpointning
to'liq manzilini ("https://sizning-domeningiz.uz/payme/webhook/") ko'rsatishingiz kerak.
"""
import base64
import json
import time

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import BoostOrder

# ---- Payme xatolik kodlari (rasmiy hujjatga muvofiq) ----
ERR_INVALID_AUTH = -32504
ERR_METHOD_NOT_FOUND = -32601
ERR_ORDER_NOT_FOUND = -31050
ERR_INVALID_AMOUNT = -31001
ERR_TRANSACTION_NOT_FOUND = -31003
ERR_UNABLE_TO_PERFORM = -31008
ERR_UNABLE_TO_CANCEL = -31007


def _rpc_error(request_id, code, message_uz, message_ru="", message_en=""):
    return JsonResponse({
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": {"uz": message_uz, "ru": message_ru or message_uz, "en": message_en or message_uz},
        },
    })


def _rpc_result(request_id, result):
    return JsonResponse({"jsonrpc": "2.0", "id": request_id, "result": result})


def _now_ms():
    return int(time.time() * 1000)


@method_decorator(csrf_exempt, name="dispatch")
class PaymeMerchantAPIView(View):
    def post(self, request):
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return _rpc_error(None, -32700, "So'rov formati noto'g'ri")

        request_id = payload.get("id")
        method = payload.get("method")
        params = payload.get("params", {}) or {}

        # ---- Autentifikatsiya: Payme "Authorization: Basic base64(Paycom:MERCHANT_KEY)" yuboradi ----
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not self._check_auth(auth_header):
            return _rpc_error(request_id, ERR_INVALID_AUTH, "Avtorizatsiya xatosi")

        handler = {
            "CheckPerformTransaction": self.check_perform_transaction,
            "CreateTransaction": self.create_transaction,
            "PerformTransaction": self.perform_transaction,
            "CancelTransaction": self.cancel_transaction,
            "CheckTransaction": self.check_transaction,
            "GetStatement": self.get_statement,
        }.get(method)

        if not handler:
            return _rpc_error(request_id, ERR_METHOD_NOT_FOUND, "Metod topilmadi")

        return handler(request_id, params)

    def _check_auth(self, auth_header):
        if not settings.PAYME_MERCHANT_KEY:
            return False
        if not auth_header.startswith("Basic "):
            return False
        try:
            decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
            login, _, password = decoded.partition(":")
        except Exception:
            return False
        return login == "Paycom" and password == settings.PAYME_MERCHANT_KEY

    def _get_order(self, params):
        account = params.get("account", {})
        order_id = account.get("order_id")
        if not order_id:
            return None
        return BoostOrder.objects.filter(pk=order_id).first()

    # ---------------- 1. CheckPerformTransaction ----------------
    def check_perform_transaction(self, request_id, params):
        order = self._get_order(params)
        if not order or order.status == "bekor_qilingan":
            return _rpc_error(request_id, ERR_ORDER_NOT_FOUND, "Buyurtma topilmadi",
                               "Заказ не найден", "Order not found")
        if params.get("amount") != order.amount:
            return _rpc_error(request_id, ERR_INVALID_AMOUNT, "Summasi noto'g'ri",
                               "Неверная сумма", "Invalid amount")
        return _rpc_result(request_id, {"allow": True})

    # ---------------- 2. CreateTransaction ----------------
    def create_transaction(self, request_id, params):
        payme_id = params.get("id")
        order = self._get_order(params)

        if not order or order.status == "bekor_qilingan":
            return _rpc_error(request_id, ERR_ORDER_NOT_FOUND, "Buyurtma topilmadi")
        if params.get("amount") != order.amount:
            return _rpc_error(request_id, ERR_INVALID_AMOUNT, "Summasi noto'g'ri")

        # Idempotentlik: shu tranzaksiya avval yaratilgan bo'lsa, o'sha ma'lumotni qaytaradi
        if order.payme_transaction_id == payme_id:
            return _rpc_result(request_id, {
                "create_time": order.payme_create_time,
                "transaction": str(order.pk),
                "state": order.payme_state,
            })

        # Boshqa faol tranzaksiya bilan band bo'lsa
        if order.payme_transaction_id and order.payme_transaction_id != payme_id and order.payme_state == 1:
            return _rpc_error(request_id, ERR_UNABLE_TO_PERFORM, "Buyurtma band qilingan")

        order.payme_transaction_id = payme_id
        order.payme_state = 1
        order.payme_create_time = _now_ms()
        order.save(update_fields=["payme_transaction_id", "payme_state", "payme_create_time"])

        return _rpc_result(request_id, {
            "create_time": order.payme_create_time,
            "transaction": str(order.pk),
            "state": 1,
        })

    # ---------------- 3. PerformTransaction ----------------
    def perform_transaction(self, request_id, params):
        payme_id = params.get("id")
        order = BoostOrder.objects.filter(payme_transaction_id=payme_id).first()
        if not order:
            return _rpc_error(request_id, ERR_TRANSACTION_NOT_FOUND, "Tranzaksiya topilmadi")

        if order.payme_state == 2:
            # Idempotent — allaqachon amalga oshirilgan
            return _rpc_result(request_id, {
                "transaction": str(order.pk), "perform_time": order.payme_perform_time, "state": 2,
            })
        if order.payme_state != 1:
            return _rpc_error(request_id, ERR_UNABLE_TO_PERFORM, "Amalga oshirib bo'lmaydi")

        order.payme_perform_time = _now_ms()
        order.payme_state = 2
        order.save(update_fields=["payme_perform_time", "payme_state"])
        order.activate()  # -> status='tolangan', 24 soatlik boost yoqiladi

        return _rpc_result(request_id, {
            "transaction": str(order.pk), "perform_time": order.payme_perform_time, "state": 2,
        })

    # ---------------- 4. CancelTransaction ----------------
    def cancel_transaction(self, request_id, params):
        payme_id = params.get("id")
        reason = params.get("reason")
        order = BoostOrder.objects.filter(payme_transaction_id=payme_id).first()
        if not order:
            return _rpc_error(request_id, ERR_TRANSACTION_NOT_FOUND, "Tranzaksiya topilmadi")

        if order.payme_state in (-1, -2):
            return _rpc_result(request_id, {
                "transaction": str(order.pk), "cancel_time": order.payme_cancel_time, "state": order.payme_state,
            })

        new_state = -2 if order.payme_state == 2 else -1
        order.payme_state = new_state
        order.payme_cancel_time = _now_ms()
        order.payme_reason = reason
        order.status = "bekor_qilingan"
        order.save(update_fields=["payme_state", "payme_cancel_time", "payme_reason", "status"])

        return _rpc_result(request_id, {
            "transaction": str(order.pk), "cancel_time": order.payme_cancel_time, "state": new_state,
        })

    # ---------------- 5. CheckTransaction ----------------
    def check_transaction(self, request_id, params):
        payme_id = params.get("id")
        order = BoostOrder.objects.filter(payme_transaction_id=payme_id).first()
        if not order:
            return _rpc_error(request_id, ERR_TRANSACTION_NOT_FOUND, "Tranzaksiya topilmadi")

        return _rpc_result(request_id, {
            "create_time": order.payme_create_time,
            "perform_time": order.payme_perform_time,
            "cancel_time": order.payme_cancel_time,
            "transaction": str(order.pk),
            "state": order.payme_state,
            "reason": order.payme_reason,
        })

    # ---------------- 6. GetStatement ----------------
    def get_statement(self, request_id, params):
        date_from = params.get("from", 0)
        date_to = params.get("to", _now_ms())
        orders = BoostOrder.objects.filter(
            payme_create_time__gte=date_from, payme_create_time__lte=date_to
        ).exclude(payme_transaction_id="")

        transactions = [{
            "id": o.payme_transaction_id,
            "time": o.payme_create_time,
            "amount": o.amount,
            "account": {"order_id": str(o.pk)},
            "create_time": o.payme_create_time,
            "perform_time": o.payme_perform_time or 0,
            "cancel_time": o.payme_cancel_time or 0,
            "transaction": str(o.pk),
            "state": o.payme_state,
            "reason": o.payme_reason,
        } for o in orders]

        return _rpc_result(request_id, {"transactions": transactions})
