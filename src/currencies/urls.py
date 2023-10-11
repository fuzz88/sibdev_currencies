from rest_framework import routers

from currencies.views import CurrencyRateViewSet, CurrencyThresholdViewSet

rates_router = routers.DefaultRouter()
rates_router.register(r"rates", CurrencyRateViewSet)

threshold_router = routers.DefaultRouter()
threshold_router.register(r"currency/user_currency", CurrencyThresholdViewSet)
