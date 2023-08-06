from enum import Enum


class ConfirmationStatus(Enum):
    NONE = "NONE"
    CONFIRMED = "CONFIRMED"
    DENIED = "DENIED"


class Slot:
    def __init__(self, name: str, value: str, confirmation_status: ConfirmationStatus):
        self.name = name
        self.value = value
        self.confirmation_status = ConfirmationStatus(confirmation_status)
        # TODO: Resolutions


class Intent:
    def __init__(self, name: str, confirmation_status: ConfirmationStatus, slots={}):
        self.name = name
        self.confirmation_status = confirmation_status
        self.slots = slots
