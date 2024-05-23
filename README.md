# MQTT Client Examples

A repository of different programming languages and libraries providing examples of MQTT Client implementations that integrate directly to the Link Labs MQTT User Credentials Object and MQTT ecosystem.

## MQTT Best Practices and Production Readiness

* Use [MQTT v5 specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html).
* Use TLS encryption and port 8883 (instead of the default, unencrypted port 1883).
* Validate TLS Certificate from Certificate Authority (no key file is required).
* Use one client id per process, sharing the same client id across multiple processes will [result in both processes disconnecting the other](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901073), preventing any messages from being processed by either process.
* Use the MQTT Shared Subscription topic, which appends a `$share/<share group>` prefix before the MQTT topic string. This allows multiple MQTT client processes, with unique MQTT client ids to "share" the same subscription, which will balance the load of traffic between the MQTT client processes. This allows for failure tolerance in the case that a subscription service fails as well as no-downtime upgrades of services by doing a rolling update of the services.
* Utilize QoS of 1 to ensure that MQTT events are received at least once (and can be possibly duplicated).
  - Utilize a `clean_session=False` when the desired behavior is to process the backlog of QoS 1 messages that were not received by the MQTT client implementation and are unacknowledged from the perspective of the Link Labs MQTT Broker.
  -  Utilize a `clean_session=True` when the desired behavior is to drop the unacknowledged and unreceived backlog messages from the Link Labs MQTT Broker and resume processing new near real time events only. 

## Getting MQTT Credentials

Once you have been registered in the Airfinder Platform with an Organization, you will need the admin level permissions to generate MQTT Crednetials.

### Via the Airfinder Platform UI

Go to the Configuration > Subscriptions menu. If this menu is not availible then your account does not have the sufficient admin level permissions.

![](https://raw.githubusercontent.com/LinkLabs/mqtt-client-examples/main/docs/airfinder_platform_mqtt_subscription_page.png)

You can view any existing credentials or "Add Subscription" to create a set of MQTT Credentials. At this point you can choose the scope of the MQTT Credentials, if the scope is for a single Airfinder Site or for the entire Organization.

![](https://github.com/LinkLabs/mqtt-client-examples/blob/main/docs/airfinder_platform_create_mqtt_subscription.png)

To view the details of an MQTT Credentials, you can click the "..." icon and select "View Details". This will allow you to copy out individual fields or export out the entire document via the "Copy All Fields" button.

![](https://github.com/LinkLabs/mqtt-client-examples/blob/main/docs/airfinder_platform_get_mqtt_credentials.png)

Once you "Copy All Fields", you can place that into a `creds.json` file within the root of the MQTT Client Example project you want to run in order to set up and run that example project.

## Via the Network Asset HTTP API

The MQTT User Credential Swagger documentation can be found here: https://networkasset-conductor.link-labs.com/networkAsset/docs.html#!/airfinder-mqttuser-controller

To utilize this API you must have an Organization level admin permission, the API accepts BasicAuth and OAuth2 (with client configuration). You must also know your Organization ID, which can be found with this endpoint: GET https://networkasset-conductor.link-labs.com/networkAsset/airfinder/organizations

When you have the organization ID you can retrieve the MQTT Credentials with

```
curl -X GET "https://networkasset-conductor.link-labs.com/networkAsset/airfinder/mqttUsers?organizationId=<organization id>" \
    -H "Authorization: basic <Basic Auth>"
```
