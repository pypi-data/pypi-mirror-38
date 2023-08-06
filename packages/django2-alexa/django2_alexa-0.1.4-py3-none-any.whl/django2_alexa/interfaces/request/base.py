import json

from django.http import HttpRequest


class BaseRequest:
    def __init__(self, request: HttpRequest):
        self._data = json.loads(request.body.decode())
        self.body = self._data['request']   # type: dict
        self.type = self.body['type']
        self.user_id = self._data["context"]["System"]["user"]["userId"]
        self.audio_player = self._data["context"]["AudioPlayer"]
