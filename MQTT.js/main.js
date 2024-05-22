const fs = require('node:fs');
function loadCreds() {
  try {
    return JSON.parse(fs.readFileSync('creds.json', 'utf8'));
  } catch (err) {
    console.error("Could not load `creds.json` file: ", err);
  }
}

creds = loadCreds()
console.log('Utilizing the following MQTT credential: ', creds);
const mqtt = require("mqtt");

client = mqtt.connect({
  host: creds.host,
  port: creds.port,
  username: creds.username,
  password: creds.password,
  clientId: creds.clientId,
  clean: false,
  protocolVersion: 5,
  protocol: 'mqtts'
});

client.on("connect", () => {
  client.subscribe(creds.topic, (err) => {
    if (err) {
      console.log("Error subscribing to topic: ", err);
      client.end()
    } else {
      console.log("Subscribed to topic!");
    }
  });
});

client.on("message", (topic, message) => {
  // message is Buffer
  console.log(message.toString());
});

client.on('error', function(err){
    console.log("ERROR: ", err)
    client.end()
})

