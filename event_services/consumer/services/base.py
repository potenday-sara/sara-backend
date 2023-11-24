import json
from abc import ABC, abstractmethod


class BaseEventService(ABC):
    def __init__(self, msg):
        self.msg = msg
        self.topic = msg.topic()
        self.key = msg.key().decode("utf-8")
        self.value = json.loads(msg.value().decode("utf-8"))

    @abstractmethod
    def execute(self):
        pass
