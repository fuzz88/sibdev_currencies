from django.db import models

from users.models import User


class CurrencyRate(models.Model):
    cbrf_id = models.CharField(max_length=10)
    num_code = models.IntegerField()
    char_code = models.CharField(max_length=3)
    name = models.CharField(max_length=256)
    nominal = models.IntegerField()
    value = models.DecimalField(max_digits=12, decimal_places=4)
    previous_value = models.DecimalField(max_digits=12, decimal_places=4)
    date = models.DateField()


class CurrencyThreshold(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    char_code = models.CharField(max_length=3)
    threshold_value = models.DecimalField(max_digits=12, decimal_places=4)
