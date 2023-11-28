from confluent_kafka import Consumer as KafkaConsumer

from event_services.consumer.services import service_class
from event_services.settings.consumer import CONSUMER_CONFIG, TOPICS


class Consumer:
    def __init__(self) -> None:
        self.config = CONSUMER_CONFIG
        self.consumer = KafkaConsumer(self.config)
        self.consumer.subscribe(TOPICS)

    def polling(self) -> None:
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue

                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                try:
                    topic = msg.topic()
                    key = msg.key().decode("utf-8")
                    print(f"topic: {topic} | key: {key}")
                    service = service_class[topic](msg)
                    service.execute()
                    del service
                except Exception as e:  # pylint: disable=broad-except
                    print(e)

        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
