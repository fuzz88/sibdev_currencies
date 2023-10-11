import json

from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User


@method_decorator(csrf_exempt, name="dispatch")
class UserRegistrationByJSON(View):
    """
    Создание нового пользователя.
    APIVersion: 1
    """

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                validate_email(data["email"])
            except:
                return HttpResponseBadRequest(f"Provided data is invalid")
            User(
                username=data[
                    "email"
                ],  # username is essential to edit User objects with default UserAdmin template
                email=data["email"],
                password=make_password(data["password"]),
            ).save()
            return HttpResponse(status=200)
        else:
            return HttpResponseBadRequest("Content-type must be application/json")


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Прокидываем свой сериализатор в SimpleJWT,
    так как родной возращает 401 код в случае неправильных логина и пароля,
    а мы, по спецификации, хотим 400.
    """

    _serializer_class = "users.serializers.CustomTokenObtainPairSerializer"
