from rest_framework import serializers

from currencies.models import CurrencyRate, CurrencyThreshold


class CurrencyRateSerializer(serializers.ModelSerializer):
    charcode = serializers.CharField(source="char_code")

    class Meta:
        model = CurrencyRate
        fields = ["id", "date", "charcode", "value"]


class CurrencyThresholdSerializer(serializers.ModelSerializer):
    currency = serializers.IntegerField(source="id")
    threshold = serializers.DecimalField(
        source="threshold_value", max_digits=12, decimal_places=4
    )

    class Meta:
        model = CurrencyThreshold
        fields = ["currency", "threshold"]
