const http = require('http');
const express = require('express');
const { WebSocketServer } = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

const PORT = process.env.PORT || 8080;

const readings = []; 
const MAX = 300;

app.use(express.json());

app.post('/webhook/temperature', (req, res) => {
  const { deviceId = 'device', celsius, timestamp } = req.body || {};
  if (typeof celsius !== 'number') {
    return res.status(400).json({ ok:false, error: 'celsius must be a number' });
  }
  const created_at = timestamp ? new Date(timestamp).toISOString() : new Date().toISOString();
  const r = { deviceId, celsius, created_at };
  readings.push(r);
  if (readings.length > MAX) readings.shift();


  const msg = JSON.stringify({ type: 'reading', data: r });
  wss.clients.forEach(c => { if (c.readyState === 1) c.send(msg); });
  res.json({ ok:true });
});


app.get('/api/temperatures', (req, res) => {
  res.json({ ok:true, rows: readings });
});


app.use(express.static('public'));

wss.on('connection', (ws) => {
  ws.send(JSON.stringify({ type: 'hello', data: 'connected' }));
});

server.listen(PORT, () => {
  console.log('listening on http://localhost:' + PORT);
});
