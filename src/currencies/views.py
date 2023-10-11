from rest_framework import viewsets
from rest_framework.response import Response

from currencies.models import CurrencyRate, CurrencyThreshold
from currencies.serializers import CurrencyRateSerializer, CurrencyThresholdSerializer


class CurrencyRateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().list(request, *args, **kwargs)
        else:
            return Response(data=[])


class CurrencyThresholdViewSet(viewsets.ModelViewSet):
    queryset = CurrencyThreshold.objects.all()
    serializer_class = CurrencyThresholdSerializer
