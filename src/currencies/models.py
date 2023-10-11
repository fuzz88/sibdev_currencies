from django.db import models

from users.models import User


class Currency(models.Model):
    cbrf_id = models.CharField(max_length=10)
    num_code = models.IntegerField()
    char_code = models.CharField(max_length=3)
    name = models.CharField(max_length=256)
    nominal = models.IntegerField()


class CurrencyRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=4)
    prev_value = models.DecimalField(max_digits=12, decimal_places=4)
    date = models.DateField()


class CurrencyThreshold(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    threshold_value = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        unique_together = (
            "user",
            "currency",
        )
