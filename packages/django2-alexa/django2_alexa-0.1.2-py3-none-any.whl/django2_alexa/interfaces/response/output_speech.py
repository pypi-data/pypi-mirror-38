from enum import Enum


class SpeechType(Enum):
    PLAIN_TEXT = "PlainText"
    SSML = "SSML"


class PlayBehavior(Enum):
    ENQUEUE = "ENQUEUE"
    REPLACE_ALL = "REPLACE_ALL"
    REPLACE_ENQUEUED = "REPLACE_ENQUEUED"


class OutputSpeech:
    def __init__(self, content: str, sp_type=SpeechType.PLAIN_TEXT, behavior=PlayBehavior.ENQUEUE):
        self.type = sp_type
        self.content = content
        self.behavior = behavior

    def to_dict(self):
        d = {
            'type': self.type.value,
            'playBehavior': self.behavior.value
        }
        if self.type == SpeechType.PLAIN_TEXT:
            d['text'] = self.content
        else:
            d['ssml'] = self.content
        return d
