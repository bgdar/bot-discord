import pika

import threading
import pika
import json
import threading
import time

from src.rabbitMQ.gateway import ClientGateway
from types import ConversiPayloadproduction


def exampelSendgatewy():
    """jangan gunakana berdamaan dengan exampelGetgatewy , bentrok inisialasiai"""
    client = ClientGateway()

    def getResultPredict(result: str):
        print("hasil predictiion : ", result)
        akhir = ConversiPayloadproduction(result)
        print("hasil akhir", akhir)

    threading.Thread(target=client.start_rabbitmq_consumer(client._getResponse, getResultPredict),
                     daemon=True).start()


def exampelGetgatewy():
    """jangan gunakana berdamaan dengan exampelSendgatewy , bentrok inisialasiai"""
    client = ClientGateway()

    client.sendText(1212, "example test dari telegram")
    client.sendText(1212, "example test dari telegram")

# # Daftarkan consumer untuk mendengarkan response
# channel.basic_consume(
#     queue=Queue.queueTelegramResponse,
#     on_message_callback=getResponse,
#     auto_ack=True
# )

# 3. SOLUSI BACKGROUND TASK: Jalankan consumer di dalam Thread terpisah
