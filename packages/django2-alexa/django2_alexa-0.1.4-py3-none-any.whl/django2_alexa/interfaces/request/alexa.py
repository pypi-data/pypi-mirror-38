from django.http import HttpRequest

from django2_alexa.interfaces.request.base import BaseRequest
from django2_alexa.interfaces.request.intent import Intent, ConfirmationStatus, Slot
from django2_alexa.utils.enums import DialogState
from django2_alexa.utils.enums.locales import Locale


class LaunchRequest(BaseRequest):
    def __init__(self, request: HttpRequest):
        super().__init__(request)
        self.request_id = self.body["requestId"]  # type: str
        self.timestamp = self.body["timestamp"]  # type: str
        self.locale = Locale(self.body["locale"])  # type: Locale
        self.session_id = self._data["session"]["sessionId"]


class IntentRequest(BaseRequest):
    def __init__(self, request: HttpRequest):
        super().__init__(request)
        self.request_id = self.body["requestId"]  # type: str
        self.timestamp = self.body["timestamp"]  # type: str
        self.locale = Locale(self.body["locale"])  # type: Locale
        self.session_id = self._data["session"]["sessionId"]
        if "dialogState" in self.body:
            self.dialog_state = DialogState(self.body["dialogState"])
        else:
            self.dialog_state = None
        intent = self.body["intent"]
        slots = {}
        if "slots" in intent:
            for name in intent["slots"]:
                slots[name] = Slot(name, intent["slots"][name]["value"],
                                   ConfirmationStatus(intent["slots"][name]["confirmationStatus"]))
        self.intent = Intent(intent["name"], ConfirmationStatus(intent["confirmationStatus"]), slots)
