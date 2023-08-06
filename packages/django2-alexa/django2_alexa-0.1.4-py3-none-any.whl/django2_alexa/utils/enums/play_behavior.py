from enum import Enum


class PlayBehavior(Enum):
    ENQUEUE = "ENQUEUE"
    REPLACE_ALL = "REPLACE_ALL"
    REPLACE_ENQUEUED = "REPLACE_ENQUEUED"
