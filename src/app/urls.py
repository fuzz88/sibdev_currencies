from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from healthchecks.views import Status
from users.views import EmailVerification, UserRegistration

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthchecks/status/", Status.as_view()),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("registration/", UserRegistration.as_view()),
    path("verification/<str:code>/", EmailVerification.as_view(), name="verification"),
]
