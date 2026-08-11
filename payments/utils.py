import base64
from django.conf import settings
from urllib.parse import quote


def build_payme_checkout_url(order_id, amount_tiyin, return_url=None):
    """
    Payme checkout (to'lov sahifasi) havolasini yaratadi.
    Hujjat: https://developer.help.paycom.uz/initsializatsiya-platezhey/
    """
    if not settings.PAYME_MERCHANT_ID:
        return None

    params = f"m={settings.PAYME_MERCHANT_ID};ac.order_id={order_id};a={amount_tiyin}"
    if return_url:
        params += f";c={return_url}"

    encoded = base64.b64encode(params.encode()).decode()
    host = "checkout.test.paycom.uz" if settings.PAYME_TEST_MODE else "checkout.paycom.uz"
    return f"https://{host}/{encoded}"
