from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.api_views import (
    RegisterAPIView, CustomTokenObtainPairView, MeAPIView,
    ProfileDetailAPIView, UpdateLocationAPIView,
)
from workers.api_views import (
    CategoryListAPIView, WorkerListAPIView, PostListCreateAPIView, PostDeleteAPIView,
)
from jobs.api_views import (
    JobListAPIView, JobCreateAPIView, MyJobsAPIView, JobToggleStatusAPIView, JobDeleteAPIView,
)
from ratings.api_views import RateWorkerAPIView, LeaderboardAPIView
from chat.api_views import (
    ConversationListAPIView, StartConversationAPIView, MessageListCreateAPIView, LiveLocationAPIView,
)

app_name = "api"

urlpatterns = [
    # ---- Auth ----
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),

    # ---- Accounts ----
    path("accounts/me/", MeAPIView.as_view(), name="me"),
    path("accounts/location/", UpdateLocationAPIView.as_view(), name="update_location"),
    path("accounts/<int:pk>/", ProfileDetailAPIView.as_view(), name="profile_detail"),

    # ---- Categories & Workers ----
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path("workers/", WorkerListAPIView.as_view(), name="worker_list"),
    path("workers/posts/", PostListCreateAPIView.as_view(), name="post_create"),
    path("workers/<int:worker_id>/posts/", PostListCreateAPIView.as_view(), name="worker_posts"),
    path("workers/posts/<int:pk>/", PostDeleteAPIView.as_view(), name="post_delete"),

    # ---- Jobs ----
    path("jobs/", JobListAPIView.as_view(), name="job_list"),
    path("jobs/yarat/", JobCreateAPIView.as_view(), name="job_create"),
    path("jobs/mening-elonlarim/", MyJobsAPIView.as_view(), name="my_jobs"),
    path("jobs/<int:pk>/holat/", JobToggleStatusAPIView.as_view(), name="job_toggle_status"),
    path("jobs/<int:pk>/", JobDeleteAPIView.as_view(), name="job_delete"),

    # ---- Ratings ----
    path("ratings/<int:worker_id>/", RateWorkerAPIView.as_view(), name="rate_worker"),
    path("ratings/reyting/", LeaderboardAPIView.as_view(), name="leaderboard"),

    # ---- Chat ----
    path("chat/conversations/", ConversationListAPIView.as_view(), name="conversations"),
    path("chat/boshlash/<int:user_id>/", StartConversationAPIView.as_view(), name="start_conversation"),
    path("chat/conversations/<int:pk>/messages/", MessageListCreateAPIView.as_view(), name="messages"),
    path("chat/conversations/<int:pk>/jonli-lokatsiya/", LiveLocationAPIView.as_view(), name="live_location"),
]
