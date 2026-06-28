import threading
import pika
import json
import time
from typing import Callable
import sys
from dataclasses import asdict

from appTypes import PayloadReceiver


class Queue:
    queueTelegram = "queue-discord"
    queueTelegramResponse = "queue-discord-response"


# Menggunakan URL koneksi yang sama
BROKER_URL = "amqp://guest:guest@localhost:5672/"
connection_params = pika.URLParameters(BROKER_URL)

# setiap method berdiri sendiri

# alur nya cuman 2
# kalau gak kirim ya menerima


class ClientGateway:
    def __init__(self):
        temp_conn = pika.BlockingConnection(connection_params)
        temp_channel = temp_conn.channel()
        temp_channel.queue_declare(queue=Queue.queueTelegram, durable=True, arguments={
            "x-queue-type": "quorum"})
        temp_channel.queue_declare(queue=Queue.queueTelegramResponse, durable=True, arguments={
            "x-queue-type": "quorum"})
        # Langsung tutup setelah selesai setup awal
        temp_conn.close()

    def sendText(self, chat_id: int, text: str):
        """Fungsi mandiri untuk mengirim pesan (Membuka koneksi baru yang aman setiap kirim)"""
        try:
            # Membuat koneksi & channel terpisah khusus untuk mengirim teks mentah
            pub_conn = pika.BlockingConnection(connection_params)
            pub_channel = pub_conn.channel()

            payload = PayloadReceiver(chat_id, text, "telegram")

            pub_channel.basic_publish(
                exchange='',
                routing_key=Queue.queueTelegram,
                body=json.dumps(asdict(payload)),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            print(
                f"[Python-Publisher] Berhasil mengirim request dari user {chat_id}")

            # Selalu tutup koneksi setelah selesai kirim data
            pub_conn.close()
        except Exception as e:
            print(f"[Python-Publisher] Gagal mengirim pesan: {e}")

    def _getResponse(self, ch, method, properties, body, getResultPredict: Callable = None):
        """Callback khusus consumer untuk menangani data masuk dari server yang menjalakan model"""
        try:
            data = json.loads(body.decode('utf-8'))
            chat_id = data.get("chat_id")
            hasil_prediksi = data.get("text")

            if getResultPredict:
                getResultPredict(hasil_prediksi)
            else:
                print("Kirim metod untuk mendapatkan hasil dari prediksi")
                sys.exit(0)

            print(
                f"[Python-Consumer] Terkessekusi! Hasil untuk user {chat_id}: {hasil_prediksi}")

            # HUBUNGKAN KE BOT TELEGRAM  DI SINI
            # bot.send_message(chat_id=chat_id, text=hasil_prediksi)

        except Exception as e:
            print(f"[Python-Consumer] Error memproses response: {e}")

    def start_rabbitmq_consumer(self, getResponse: Callable = None, getResultPredict: Callable = None):
        """Fungsi ini akan mengunci koneksinya sendiri di dalam thread terpisah
              Example : 
               # 2. Jalankan Consumer di latar belakang (Memiliki koneksi/channel-nya sendiri)
                threading.Thread(target=start_rabbitmq_consumer, daemon=True).start()

                # Beri jeda 1 detik agar thread background benar-benar terhubung ke RabbitMQ dahulu
                time.sleep(1) """

        print(
            "[Python-Consumer] Consumer RabbitMQ bersiap berjalan di latar belakang...")
        try:
            # Koneksi mandiri khusus untuk mendengarkan data, tidak akan diganggu oleh sendText
            sub_conn = pika.BlockingConnection(connection_params)
            sub_channel = sub_conn.channel()

            if getResponse and getResultPredict:

                sub_channel.basic_consume(
                    queue=Queue.queueTelegramResponse,
                    # gunakna lamda untuk menitimm method untuk mendapatkan data
                    on_message_callback=lambda ch, method, properties, body, : getResponse(
                        ch, method, properties, body, Callable),
                    auto_ack=True
                )
            else:
                print(
                    "Kirim response calabel dari method getResponse() dan juga method untuk mendapatkan hasil prediksi")
                sys.exit(0)

            print(
                "[Python-Consumer] Consumer RabbitMQ AKTIF mendengarkan di latar belakang.")
            sub_channel.start_consuming()
        except Exception as e:
            print(f"[Python-Consumer] Terjadi error fatal pada consumer: {e}")


# if __name__ == "__main__":
#     # 1. Pastikan Queue sudah terbuat dengan aman
#     initQueue()
#     print("[Python] Inisialisasi Queue selesai.")
#
#     # 2. Jalankan Consumer di latar belakang (Memiliki koneksi/channel-nya sendiri)
#     threading.Thread(target=start_rabbitmq_consumer, daemon=True).start()
#
#     # Beri jeda 1 detik agar thread background benar-benar terhubung ke RabbitMQ dahulu
#     time.sleep(1)
#
#     # 3. Simulasi Kirim data dari User Telegram (Sangat aman karena membuka channel baru)
#     sendText(112121, "Halo ini pesan mentah dari user Telegram")
#     sendText(1222121, "Halo ini pesan mentah dari user Telegram 2")
#
#     # Loop penahan agar program utama/bot  tidak mati
#     while True:
#         time.sleep(1)
