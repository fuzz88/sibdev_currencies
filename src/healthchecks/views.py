from django.http import JsonResponse
from django.views import View


class Status(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "online"})
