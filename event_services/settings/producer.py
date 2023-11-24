from event_services.settings.base import *  # noqa

PRODUCER_CONFIG = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "client.id": "sara-producer",
}
