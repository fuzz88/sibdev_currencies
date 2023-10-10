from rest_framework import routers

from currencies.views import CurrencyRateViewSet

rates_router = routers.DefaultRouter()
rates_router.register(r"rates", CurrencyRateViewSet)
