# Satu Sirviön IoT-harkat 
Tämä projekti sisältää eri luentojen harjoituskoodit ja materiaalit IoT-perusteiden kurssilta.  

## Sisältö

- **Luento 1** – Python-esimerkkejä (LEDin ohjaus, hälytykset, sääasema).
- **Luento 2** – Node.js-palvelin ja WiFi-ohjelmointi.
- **Luento 3** – Node.js-palvelin (server2).
- **Luento 4** – Tuntiharjoitukset sekä oma järjestelmä
  - `device/` – laitteen ohjelmakoodi (Python)
  - `public/` – selainpohjainen käyttöliittymä  
  - `server.js` – palvelin
  - `README.md` – lisätietoa   

## Kansiorakenne
```
IoT-perusteet/
├── Luento 1/
│ ├── blink_the_led.py
│ ├── burglary_alarm.py
│ ├── interup.py
│ ├── play_around.py
│ ├── traffic_lights.py
│ ├── turn_the_led_on
│ ├── weather_station.py
│ └── weather_station_2.py
│
├── Luento 2/
│ ├── server1.js
│ └── wifi.py
│
├── Luento 3/
│ └── server2.js
│
├── Luento 4/
│ ├── device/
│ │ └── wokwi.py
│ ├── public/
│ │ ├── fetch_temperature.html
│ │ ├── fetch_temperature.js
│ │ └── index.html
│ ├── server.js
│ └── README.md
│
├── node_modules/
│
├── .gitignore
├── package.json
├── package-lock.json
└── README.md       
