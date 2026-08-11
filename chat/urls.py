from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("chat/", views.inbox_view, name="inbox"),
    path("chat/boshlash/<int:user_id>/", views.start_conversation_view, name="start_conversation"),
    path("chat/<int:pk>/", views.conversation_view, name="conversation"),
    path("chat/<int:pk>/yuborish/", views.send_message_view, name="send_message"),
    path("chat/<int:pk>/yangilarini-olish/", views.fetch_messages_view, name="fetch_messages"),
    path("chat/<int:pk>/jonli-lokatsiya/", views.live_location_page_view, name="live_location"),
    path("chat/<int:pk>/jonli-lokatsiya/malumot/", views.live_locations_data_view, name="live_location_data"),
]
