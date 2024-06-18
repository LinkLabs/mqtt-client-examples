class MQTTCredentials {
  host = "";
  port = 8883;
  username = "";
  password = "";
  clientId = "";
  topic = "";
  // Non required attributes
  protocol = "";
  organizationId = "";
  subscriptionDate = "";
  userId = 0;
  isEnabled = 0;
  subscriptionType = "";
}

const fs = require('node:fs');
function loadCreds() {
  try {
    return Object.assign(new MQTTCredentials, JSON.parse(fs.readFileSync('creds.json', 'utf8')))
  } catch (err) {
    console.error("Could not load `creds.json` file: ", err);
  }
}

creds = loadCreds()
console.log('Utilizing: MQTTCredentials', JSON.stringify(creds, null, 4));

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
  client.subscribe([creds.topic], {qos: 1}, (err, granted) => {
    if (err) {
      console.error(err);
      client.end()
    } else {
      granted.forEach(granted_sub => {
        console.log("Subscribed to topic", granted_sub.topic, "using a QoS of", granted_sub.qos,"!");
        console.log()
      });
    }
  });
});

client.on("disconnect", (packet) => {
  console.debug(packet)
  console.log("Disconnected!", mqtt.ReasonCodes[packet.reasonCode])
})

client.on("message", (topic, message) => {
  // message is Buffer
  console.log(topic, "->", JSON.parse(message.toString()));
});

client.on('error', function(err){
    console.error(err)
    client.end()
})

