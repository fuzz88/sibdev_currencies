from django.contrib import admin
from django.urls import include, path

from healthchecks.views import Status
from users.views import CustomTokenObtainPairView, UserRegistrationByJSON

service_urls = [
    path("admin/", admin.site.urls),
    path("healthchecks/status/", Status.as_view()),
]


v1_API_urls = [
    path("user/register/", UserRegistrationByJSON.as_view(), name="create_user"),
    path("user/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = [
    path("api/v1/", include(v1_API_urls)),
    path("", include(service_urls)),
]
