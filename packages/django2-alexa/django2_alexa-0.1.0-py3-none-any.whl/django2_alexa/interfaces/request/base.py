import json

from django.http import HttpRequest


class BaseRequest:
    def __init__(self, request: HttpRequest):
        self.body = json.loads(request.body.decode())   # type: dict
