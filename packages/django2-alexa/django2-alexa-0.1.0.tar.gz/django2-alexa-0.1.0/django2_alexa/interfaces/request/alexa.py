from django.http import HttpRequest

from django2_alexa.interfaces.request.base import BaseRequest
from django2_alexa.utils.alexa.locales import Locale


class LaunchRequest(BaseRequest):
    def __init__(self, request: HttpRequest):
        super().__init__(request)
        self.type = "LaunchRequest"
        self.request_id = self.body["requestId"]    # type: str
        self.timestamp = self.body["timestamp"]     # type: str
        self.locale = Locale(self.body["locale"])   # type: Locale
