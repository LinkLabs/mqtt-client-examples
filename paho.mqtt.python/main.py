#!/usr/bin/python3

from dataclasses import dataclass
import json
import logging
import os
from typing import Optional


logging.basicConfig()
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)


@dataclass
class MQTTCredentials:
    host: str
    port: str
    clientId: str
    username: str
    password: str
    topic: str
    # Non required Attributes
    organizationId: str
    protocol: str
    subscribeAcl: str
    publishAcl: Optional[str]
    subscriptionDate: str
    userId: int
    isEnabled: int
    subscriptionType: str


def load_creds() -> MQTTCredentials:
    with open('creds.json') as creds_file: 
        return MQTTCredentials(**json.load(creds_file))


creds = load_creds()
LOG.info(f"Using {creds}")


import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, flags, reason_code, properties=None):
    LOG.debug("Connect Return Code: " + reason_code.getName())


def on_message(mqttc, obj, msg):
    LOG.info(f"{msg.topic} -> {json.dumps(json.loads(msg.payload), sort_keys=True, indent=4)}")

def on_subscribe(mqttc, userdata, mid, reason_codes, properties):
    LOG.info(f"Subscribed: {str(mid)} {[code.getName() for code in reason_codes]}")


def on_log(mqttc, obj, level, string):
    LOG.debug(string)


def on_disconnect(mqttc, obj, flags, reason_code, properties=None):
    if flags != 0:
        LOG.error(f"Unexpected DISCONNECT: {mqtt.error_string(flags)} | {reason_code}")
    else:
        LOG.info(f"Disconnected Successfully: {mqtt.error_string(flags)}")

# Create MQTT Client Instance
mqttc = mqtt.Client(client_id=creds.clientId, protocol=mqtt.MQTTv5)
mqttc.username_pw_set(username=creds.username, password=creds.password)
mqttc.tls_set()

# Register MQTT Callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
# Comment to disable debug messages
mqttc.on_log = on_log

# Establish MQTT Connection and run application loop
mqttc.connect(host=creds.host, port=int(creds.port), keepalive=60)
ret = mqttc.subscribe(creds.topic, qos=1)
try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    LOG.info("Disconnecting from client...")
    mqttc.disconnect()

