const url = "https://api.thingspeak.com/channels/<CHANNEL_ID>/feeds.json?results=100";

fetch(url)
  .then(response => response.json())
  .then(data => {
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
  })
  .catch(err => {
    console.error(err);
    document.getElementById("output").textContent = "Error loading data";
  });
