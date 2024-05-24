import config

import time
import ubinascii
import network
from machine import unique_id
from umqtt.simple import MQTTClient

WIFI_SSID = config.WIFI_SSID
WIFI_PASSWORD = config.WIFI_PASSWORD

CLIENT_ID = ubinascii.hexlify(unique_id())
SERVER = config.SERVER_MQTT_BROKER

TOPIC_PREFIX = "i483/sensors/2410064"

station_if = network.WLAN(network.STA_IF)

station_if.active(True)
time.sleep(2)
station_if.connect(WIFI_SSID, WIFI_PASSWORD)
print("Successfully connected to Wi-Fi!")
print('Network config:', station_if.ifconfig())

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()
print(f"Connected to MQTT Broker {SERVER}")

topics = [
    f"{TOPIC_PREFIX}/SCD41/co2",
    f"{TOPIC_PREFIX}/SCD41/humidity",
    f"{TOPIC_PREFIX}/SCD41/temperature",
    f"{TOPIC_PREFIX}/BMP180/temperature",
    f"{TOPIC_PREFIX}/BMP180/air_pressure"
]

def main():
    client.set_callback(read_message)
    for topic in topics:
        client.subscribe(topic)

    while True:
        client.check_msg()
        time.sleep(1)

def read_message(topic, message):
    print(f"{topic.decode()}: {message.decode()}")

main()
