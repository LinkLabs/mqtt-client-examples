#!/usr/bin/python3

from dataclasses import dataclass
import json
import os
from typing import Optional


@dataclass
class MQTTCredentials:
    clientId: str
    host: str
    organizationId: str
    password: str
    port: str
    protocol: str
    subscribeAcl: str
    publishAcl: Optional[str]
    subscriptionDate: str
    topic: str
    userId: int
    username: str
    isEnabled: int
    subscriptionType: str


def load_creds() -> MQTTCredentials:
    with open('creds.json') as creds_file: 
        return MQTTCredentials(**json.load(creds_file))


creds = load_creds()
print(f"Using {creds}")


import paho.mqtt.client as mqtt


def on_connect(mqttc, userdata, flags, rc, properties=None):
    print("rc: " + rc.getName())


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_subscribe(mqttc, userdata, mid, reason_codes, properties):
    print(f"Subscribed: {str(mid)} {[code.getName() for code in reason_codes]}")


def on_log(mqttc, obj, level, string):
    print(string)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print()
        client.on_log(userdata, "error", f"{rc}", f"Unexpected DISCONNECT: {mqtt.error_string(rc)}")


mqttc = mqtt.Client(client_id=creds.clientId, protocol=mqtt.MQTTv5)
mqttc.username_pw_set(username=creds.username, password=creds.password)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

# Comment to disable debug messages
mqttc.on_log = on_log

mqttc.tls_set()
mqttc.connect(host=creds.host, port=int(creds.port), keepalive=60)
ret = mqttc.subscribe(creds.topic, qos=1)
mqttc.loop_forever()

