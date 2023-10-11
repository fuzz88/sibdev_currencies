from django.db.models import Case, F, Value, When
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from currencies.models import CurrencyRate, CurrencyThreshold
from currencies.serializers import CurrencyRateSerializer, CurrencyThresholdSerializer


class CurrencyRateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # для неавторизированного пользователя стандарный рид-онли ответ
            return super().list(request, *args, **kwargs)
        else:
            # для авторизированного делаем джоин с таблицей пороговых значений
            user_id = request.user.id
            queryset = self.get_queryset()

            serializer = self.get_serializer(
                queryset.filter(
                    currency_id__in=CurrencyThreshold.objects.filter(
                        user_id=user_id
                    ).values_list("currency_id", flat=True)
                )
                .annotate(
                    is_above_threshold=Case(
                        When(
                            value__gt=F("currency__currencythreshold__threshold_value"),
                            then=Value(True),
                        ),
                        default=Value(False),
                    )
                )
                .select_related("currency")
                .values(
                    "id",
                    "value",
                    "date",
                    "currency__id",
                    "currency__char_code",
                    "is_above_threshold",
                ),
                many=True,
            )
            return Response(serializer.data)


class CurrencyThresholdViewSet(viewsets.ModelViewSet):
    queryset = CurrencyThreshold.objects.all()
    serializer_class = CurrencyThresholdSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CurrencyThreshold(
            currency_id=serializer.data["currency"],
            threshold_value=serializer.data["threshold"],
            user_id=request.user.id,
        ).save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
