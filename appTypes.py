from dataclasses import dataclass
import json

# Type type yang akan di guakan di Bot App ini

# nantik tinggal assdict


@dataclass
class PayloadReceiver:
    """gunaka untuk mengirim data ke queue-discord rabbitMq """
    chat_id: str
    text: str
    platfrom: str


def ConversiPayloadReceiver(data:  str) -> PayloadReceiver:
    parseData = json.loaddata(data)
    return PayloadReceiver(**parseData)


@dataclass
class PayloadProducer:
    """gunaka untuk mengirim data ke queue-discord rabbitMq """
    chat_id: str
    text: str
    plafrom: str


def ConversiPayloadproduction(data:  str) -> PayloadReceiver:
    parseData = json.loaddata(data)
    return PayloadProducer(**parseData)
