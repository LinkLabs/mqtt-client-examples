# Errata

## MQTT.js handling failed subscription requests

Status: Issue Identified, PR requested.

### Related Tickets

- https://github.com/mqttjs/MQTT.js/issues/1510

### Expeted MQTT Behavior

> The Payload contains a list of Reason Codes. Each Reason Code corresponds to a Topic Filter in the SUBSCRIBE packet being acknowledged. The order of Reason Codes in the SUBACK packet MUST match the order of Topic Filters in the SUBSCRIBE packet [MQTT-3.9.3-1].

|Value|Hex|Reason Code name|Description|
|--- |--- |--- |--- |
|0|0x00|Granted QoS 0|The subscription is accepted and the maximum QoS sent will be QoS 0. This might be a lower QoS than was requested.|
|1|0x01|Granted QoS 1|The subscription is accepted and the maximum QoS sent will be QoS 1. This might be a lower QoS than was requested.|
|2|0x02|Granted QoS 2|The subscription is accepted and any received QoS will be sent to this subscription.|
|128|0x80|Unspecified error|The subscription is not accepted and the Server either does not wish to reveal the reason or none of the other Reason Codes apply.|
|131|0x83|Implementation specific error|The SUBSCRIBE is valid but the Server does not accept it.|
|135|0x87|Not authorized|The Client is not authorized to make this subscription.|
|143|0x8F|Topic Filter invalid|The Topic Filter is correctly formed but is not allowed for this Client.|
|145|0x91|Packet Identifier in use|The specified Packet Identifier is already in use.|
|151|0x97|Quota exceeded|An implementation or administrative imposed limit has been exceeded.|
|158|0x9E|Shared Subscriptions not supported|The Server does not support Shared Subscriptions for this Client.|
|161|0xA1|Subscription Identifiers not supported|The Server does not support Subscription Identifiers; the subscription is not accepted.|
|162|0xA2|Wildcard Subscriptions not supported|The Server does not support Wildcard Subscriptions; the subscription is not accepted.|

> The Server sending a SUBACK packet MUST use one of the Subscribe Reason Codes for each Topic Filter received [MQTT-3.9.3-2].
 
> Non-normative comment
>
> There is always one Reason Code for each Topic Filter in the corresponding SUBSCRIBE packet. If the Reason Code is not specific to a Topic Filters (such as 0x91 (Packet Identifier in use)) it is set for each Topic Filter.

https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901178

### Expected MQTT.js Library Client Behavior

When the MQTT Broker issues a [Reason Code](https://github.com/mqttjs/MQTT.js/blob/main/src/lib/handlers/ack.ts#L5) greater or equal to 0x128, it is an error and should be identified as such.

The subscribe method has the following signature: 

> mqtt.Client#subscribe(topic/topic array/topic object, [options], [callback])

and accepts a callback function to handle the results of the subscription request.

> callback - `function (err, granted)` callback fired on suback where:
>   - `err` a subscription error or an error that occurs when client is disconnecting
>   - `granted` is an array of `{topic, qos}` where:
>      - `topic` is a subscribed to topic
>      - `qos` is the granted QoS level on it

### Actual Behavior

When the MQTT Client fails to subscribe to a topic (retrieves a Return Code > 0x128):
- the `err` attribute is not set (`null`)
- the [Error Event](https://github.com/mqttjs/MQTT.js?tab=readme-ov-file#event-error) is not triggered.

Instead, the suback return code is always assumed to be successful and is returned as the QoS, which is valid for return code 0x00, 0x01, 0x02, but is not valid for return code greater than 0x128.

For example, if an MQTT client requests to subscribe to a topic they do not have access to, the MQTT broker will respond with an error code '135': 'Not authorized'.

In this example, the on_subscribe callback will be called with the following parameters:

```
error: null,
granted:[
  {
    topic: 'topic/that/client/doesnt/have/permission/for',
    qos: 135,
    nl: false,
    rap: false,
    rh: 0,
    properties: undefined
  }
]
```

When it should be called with

```
error: 135,
granted: null
```
