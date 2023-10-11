from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from currencies.models import CurrencyRate, CurrencyThreshold
from currencies.serializers import CurrencyRateSerializer, CurrencyThresholdSerializer


class CurrencyRateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer
    permission_classes = IsAuthenticatedOrReadOnly

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # для неавторизированного пользователя стандарный рид-онли ответ
            return super().list(request, *args, **kwargs)
        else:
            # для авторизированного делаем джоин с таблицей пороговых значений
            # TODO
            return Response(data=[])


class CurrencyThresholdViewSet(viewsets.ModelViewSet):
    queryset = CurrencyThreshold.objects.all()
    serializer_class = CurrencyThresholdSerializer
    permission_classes = IsAuthenticated
