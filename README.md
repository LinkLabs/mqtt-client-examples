# MQTT Client Examples

A repository of different programming languages and libraries providing examples of MQTT implementations that integrate directly to the Link Labs MQTT Credentials Object and MQTT ecosystem.

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
