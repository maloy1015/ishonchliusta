from django.urls import path
from . import views
from .payme_api import PaymeMerchantAPIView

app_name = "payments"

urlpatterns = [
    path("tezkor-xizmat/usta/", views.boost_worker_profile_view, name="boost_worker"),
    path("tezkor-xizmat/ish/<int:job_id>/", views.boost_job_view, name="boost_job"),
    path("tolov/<int:order_id>/", views.checkout_view, name="checkout"),
    path("tolov/<int:order_id>/qaytish/", views.return_page_view, name="return_page"),

    # Payme serveri murojaat qiladigan webhook (login talab qilinmaydi, Basic Auth bilan himoyalangan)
    path("payme/webhook/", PaymeMerchantAPIView.as_view(), name="payme_webhook"),
]
