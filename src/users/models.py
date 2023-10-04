from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = "email"
    email = models.EmailField(unique=True, blank=False)
    REQUIRED_FIELDS = ["username"]
