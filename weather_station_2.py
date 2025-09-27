import network
import time
import urequests
import dht
from machine import Pin

SSID = "Wokwi-GUEST"     
PASSWORD = ""             

THINGSPEAK_API_KEY = "XXXXX" 
THINGSPEAK_URL = "https://api.thingspeak.com/update"

sensor = dht.DHT22(Pin(15))

def connect_wifi(ssid: str, password: str, timeout_s: int = 30) -> bool:
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

def send_to_thingspeak(temp_c: float | None, hum_pct: float | None) -> None:
    if temp_c is None and hum_pct is None:
        print("Nothing to send (temp and humidity are None)")
        return
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

    except OSError as e:
        print("Sensor read error:", e)
    except Exception as e:
        print("Unexpected error:", e)

    time.sleep(PUBLISH_INTERVAL_S)
