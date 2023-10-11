from rest_framework import serializers

from currencies.models import CurrencyRate, CurrencyThreshold


class CurrencyRateSerializer(serializers.ModelSerializer):
    charcode = serializers.CharField(source="currency.char_code")
    is_above_threshold = serializers.BooleanField(required=False)

    class Meta:
        model = CurrencyRate
        fields = ["id", "date", "charcode", "value", "is_above_threshold"]


class CurrencyThresholdSerializer(serializers.ModelSerializer):
    currency = serializers.IntegerField(source="currency.id")
    threshold = serializers.DecimalField(
        source="threshold_value", max_digits=12, decimal_places=4
    )

    class Meta:
        model = CurrencyThreshold
        fields = ["currency", "threshold"]
