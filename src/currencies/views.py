from rest_framework import serializers, viewsets
from rest_framework.response import Response

from currencies.models import CurrencyRate, CurrencyThreshold


class CurrencyRateSerializer(serializers.ModelSerializer):
    charcode = serializers.CharField(source="char_code")

    class Meta:
        model = CurrencyRate
        fields = ["id", "date", "charcode", "value"]


class CurrencyRateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().list(request, *args, **kwargs)
        else:
            return Response(data=[])


class CurrencyThresholdSerializer(serializers.ModelSerializer):
    currency = serializers.IntegerField(source="id")
    threshold = serializers.DecimalField(
        source="threshold_value", max_digits=12, decimal_places=4
    )

    class Meta:
        model = CurrencyThreshold
        fields = ["currency", "threshold"]
