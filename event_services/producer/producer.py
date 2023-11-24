import json
from typing import Any

from confluent_kafka import Producer as KafkaProducer

from event_services.settings.producer import PRODUCER_CONFIG


class Producer:
    def __init__(self) -> None:
        self.config = PRODUCER_CONFIG
        self.producer = KafkaProducer(self.config)

    def produce(self, topic: str, key: str, value: dict[str, Any]) -> None:
        key_bytes: bytes = key.encode("utf-8")
        value_bytes: bytes = json.dumps(value).encode("utf-8")
        self.producer.produce(topic, key=key_bytes, value=value_bytes)
        self.producer.flush()
