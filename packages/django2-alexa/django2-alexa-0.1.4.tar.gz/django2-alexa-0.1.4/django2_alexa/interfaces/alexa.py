from django.conf import settings
from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from django2_alexa.interfaces.request.alexa import LaunchRequest, IntentRequest
from django2_alexa.interfaces.request.audio_player import PlaybackRequest, PlaybackFailedRequest
from django2_alexa.interfaces.request.base import BaseRequest
from django2_alexa.utils.s3_verification import is_valid_request


class Skill:
    # Standard
    _launch = None
    _intents = {}

    # AudioPlayer
    _playback_started = None
    _playback_finished = None
    _playback_stopped = None
    _playback_nearly_finished = None
    _playback_failed = None

    def __init__(self):
        self.view = csrf_exempt(self._view)

    def _view(self, request, *args, **kwargs):
        re = BaseRequest(request)

        # Standard Requests
        if re.type == "LaunchRequest" and self._launch:
            return self._launch(request, *args, **kwargs)
        if re.type == "IntentRequest":
            name = re.body['intent']['name']
            if name in self._intents:
                return self._intents[name](request, *args, **kwargs)

        # AudioPlayer Requests
        if re.type == "AudioPlayer.PlaybackStarted" and self._playback_started:
            return self._playback_started(request, *args, **kwargs)
        if re.type == "AudioPlayer.PlaybackFinished" and self._playback_started:
            return self._playback_finished(request, *args, **kwargs)
        if re.type == "AudioPlayer.PlaybackStopped" and self._playback_started:
            return self._playback_stopped(request, *args, **kwargs)
        if re.type == "AudioPlayer.PlaybackNearlyFinished" and self._playback_started:
            return self._playback_nearly_finished(request, *args, **kwargs)
        if re.type == "AudioPlayer.PlaybackFailed" and self._playback_started:
            return self._playback_failed(request, *args, **kwargs)

        return HttpResponseServerError("Request not implemented.")

    @staticmethod
    def _wrapper(func, req):
        def wrapper(request, *args, **kwargs):
            if getattr(settings, "ALEXA_VERIFY_CONN", False) and not is_valid_request(request):
                return HttpResponseServerError("Amazon Server verification failed.")
            alexa_request = req(request)
            return func(alexa_request, *args, **kwargs)
        return wrapper

    # Standard
    def launch(self, func):
        wrapper = self._wrapper(func, LaunchRequest)
        self._launch = wrapper
        return wrapper

    def intent(self, name: str):
        def inner(func):
            wrapper = self._wrapper(func, IntentRequest)
            self._intents[name] = wrapper
            return wrapper
        return inner

    # AudioPlayer
    def playback_started(self, func):
        wrapper = self._wrapper(func, PlaybackRequest)
        self._playback_started = wrapper
        return wrapper

    def playback_finished(self, func):
        wrapper = self._wrapper(func, PlaybackRequest)
        self._playback_finished = wrapper
        return wrapper

    def playback_stopped(self, func):
        wrapper = self._wrapper(func, PlaybackRequest)
        self._playback_stopped = wrapper
        return wrapper

    def playback_nearly_finished(self, func):
        wrapper = self._wrapper(func, PlaybackRequest)
        self._playback_nearly_finished = wrapper
        return wrapper

    def playback_failed(self, func):
        wrapper = self._wrapper(func, PlaybackFailedRequest)
        self._playback_nearly_finished = wrapper
        return wrapper
