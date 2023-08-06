from django.conf import settings
from django.http import HttpResponseServerError

from django2_alexa.interfaces.request.alexa import LaunchRequest
from django2_alexa.utils.s3_verification import is_valid_request


def launch(func):
    def wrapper(request, *args, **kwargs):
        if getattr(settings, "ALEXA_VERIFY_CONN", False) and not is_valid_request(request):
            # TODO: Troubleshooting part in docs
            return HttpResponseServerError("Amazon Server verification failed.")
        lr = LaunchRequest(request)
        return func(request, lr, *args, **kwargs)
    return wrapper


def intent(name: str):
    def inner(func):
        def wrapper(request, *args, **kwargs):
            if getattr(settings, "ALEXA_VERIFY_CONN", False) and not is_valid_request(request):
                return HttpResponseServerError("Amazon Server verification failed.")
            return func(request, *args, **kwargs)
        return wrapper
    return inner
