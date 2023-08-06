from django.http import HttpRequest

from django2_alexa.interfaces.request.base import BaseRequest
from django2_alexa.utils.enums import Locale


class PlaybackRequest(BaseRequest):
    def __init__(self, request: HttpRequest):
        super().__init__(request)
        self.request_id = self.body["requestId"]  # type: str
        self.timestamp = self.body["timestamp"]  # type: str
        self.locale = Locale(self.body["locale"])  # type: Locale
        self.token = self.body["token"]
        self.offset = self.body["offsetInMilliseconds"]


class PlaybackState:
    def __init__(self, token: str, offset: int, player_activity):
        self.token = token
        self.offset = offset
        self.player_activity = player_activity


class PlaybackFailedRequest(PlaybackRequest):
    def __init__(self, request: HttpRequest):
        super().__init__(request)
        # TODO: ´player_activity´ and ´error_type´ should be from enum (not str):
        # TODO: https://developer.amazon.com/de/docs/custom-skills/audioplayer-interface-reference.html#playbackfailed
        self.error_type = self.body["error"]["type"]
        self.error_message = self.body["error"]["message"]
        self.current_playback_state = PlaybackState(self.body["currentPlaybackState"]["token"],
                                                    self.body["currentPlaybackState"]["offset"],
                                                    self.body["currentPlaybackState"]["playerActivity"])
