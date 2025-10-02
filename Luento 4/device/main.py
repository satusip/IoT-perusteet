import network
import time
import urequests
import dht
from machine import Pin
import json

SSID = "Wokwi-GUEST"
PASSWORD = ""

# ThingSpeak 
THINGSPEAK_API_KEY = "XXXXX"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Oma webhook 
WEBHOOK_URL = "XXXXX"

sensor = dht.DHT22(Pin(15))

def connect_wifi(ssid, password, timeout_s=30):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi", end="")
        wlan.connect(ssid, password)
        start = time.ticks_ms()
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.5)
            if time.ticks_diff(time.ticks_ms(), start) > timeout_s * 1000:
                print("\nWi-Fi connect timeout")
                return False
        print("\nConnected. IP:", wlan.ifconfig()[0])
    else:
        print("Wi-Fi already connected. IP:", wlan.ifconfig()[0])
    return True

def send_to_thingspeak(temp_c, hum_pct):
    try:
        payload = "api_key={}&field1={}&field2={}".format(
            THINGSPEAK_API_KEY,
            "" if temp_c is None else temp_c,
            "" if hum_pct is None else hum_pct,
        )
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = urequests.post(THINGSPEAK_URL, data=payload, headers=headers)
        print("ThingSpeak response:", resp.text)
        resp.close()
    except Exception as e:
        print("Failed to send to ThingSpeak:", e)

def send_to_webhook(temp_c, hum_pct):
    try:
        payload = {"deviceId": "esp32-dht22", "celsius": float(temp_c)}
        headers = {"Content-Type": "application/json"}
        resp = urequests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        print("Webhook response:", resp.status_code)
        resp.close()
    except Exception as e:
        print("Failed to send to webhook:", e)

connect_wifi(SSID, PASSWORD)

PUBLISH_INTERVAL_S = 15

while True:
    try:
        wlan = network.WLAN(network.STA_IF)
        if not wlan.isconnected():
            print("Wi-Fi disconnected, reconnecting…")
            if not connect_wifi(SSID, PASSWORD):
                time.sleep(PUBLISH_INTERVAL_S)
                continue

        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        print("Temperature: {:.1f}°C".format(temperature))
        print("Humidity: {:.1f}%".format(humidity))

        send_to_thingspeak(temperature, humidity)
        send_to_webhook(temperature, humidity)

    except OSError as e:
        print("Sensor read error:", e)
    except Exception as e:
        print("Unexpected error:", e)

    time.sleep(PUBLISH_INTERVAL_S)
