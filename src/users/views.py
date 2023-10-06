from django.db import IntegrityError
import jwt
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.hashers import make_password

from app.settings import SECRET_KEY
from users.forms import UserRegistrationForm
from users.models import User


class UserRegistration(View):
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # don't want to save such intermediate information anywhere on backend.
            # very very very unsecure approach. made for lulz.
            # excessive jwt is a VULNERABILITY.

            code = jwt.encode(
                {
                    "email": form.data.get("email"),
                    "password": form.data.get("password"),
                },
                key=SECRET_KEY,
                algorithm="HS256",
            )
            return render(
                request, "after-registration.html", {"verification_code": code}
            )
        return redirect("https://www.berkeley.edu/")

    def get(self, request, *args, **kwargs):
        return render(request, "registration.html", {"form": UserRegistrationForm})


class EmailVerification(View):
    def get(self, request, code=None, *args, **kwargs):
        try:
            decoded = jwt.decode(code, key=SECRET_KEY, algorithms="HS256")
        except:
            return HttpResponseBadRequest()
        try:
            User(
                username=decoded["email"],
                email=decoded["email"],
                password=make_password(decoded["password"]),
            ).save()
            return HttpResponse("Registration Successful!")
        except IntegrityError:
            return HttpResponse("Registration Failed!")
