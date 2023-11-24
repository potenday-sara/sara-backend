from event_services.settings.base import *  # noqa

CONSUMER_CONFIG = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "group.id": "sara",
    "auto.offset.reset": "earliest",
}

TOPICS = ["question"]
