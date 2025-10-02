# Huonelämpötilaprojekti 
Pipeline:
**Wowki** → **ThingSpeak** *ja/ tai* **oma kevyt Node-palvelin (Webhook + WebSocket)** → **dashboard**

## Sisältö
```
.
├─ server.js             
├─ public/
│  ├─ index.html         
│  ├─ fetch_temperature.html
│  └─ fetch_temperature.js
└─ device/
   └─ wokwi.py             

## 1) Palvelin 
```bash
npm init -y
npm i express ws
node server.js
# selaimella: http://localhost:8080
```
- `POST /webhook/temperature` – JSON:
  ```json
  { "deviceId": "esp32-dht22", "celsius": 22.5 }
  ```
- `GET /api/temperatures` – palauttaa listan kaaviolle.
- WebSocket: sama portti, dashboard päivittää pisteet **reaaliaikaisesti**.

## 2) Dashboard
- Avaa `http://localhost:8080` → `public/index.html`
- Hakee alkuhistorian `/api/temperatures` ja kuuntelee WebSocketia uusille näytteille.

## 3) ThingSpeak
- Avaa `public/fetch_temperature.js` ja korvaa muuttujaan suora linkki.
- Avaa `public/fetch_temperature.html` selaimessa nähdäksesi JSONin.

## 4) Laite – MicroPython (Wokwi)
`device/wokwi.py` 

Muokkaa nämä:
```python
SSID = "Wokwi-GUEST"
PASSWORD = ""
THINGSPEAK_API_KEY = "XXXXX"

WEBHOOK_URL = "oma url" 
```
