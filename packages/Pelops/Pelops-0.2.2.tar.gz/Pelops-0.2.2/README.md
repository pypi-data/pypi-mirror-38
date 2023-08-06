# Overview

Pelops is a set of microservices that are coupled via mqtt. The idea is to provide small programs that are configured and drive raspberry pi controlled sensors and actuators. Thus - ideally - rich solutions can be built without any programming and with little engineering efford. It can be used for example to make a stand alone solution on one raspi, make a distributed system where several devices interact (maybe even via internet services like AWS IoT), or interact with home automation systems like openhab. Focus is on ePapers for display devices (currently supported are three epapers/einks from Waveshare).

![Component Overview](img/Microservice Overview.png)

Currently, the following microservices are available:
 * [Alcathous](https://gitlab.com/pelops/alcathous) - This software subscribes to mqtt-topics that contain raw sensor data and publishes average values for configurable time spans.
 * [Argaeus](https://gitlab.com/pelops/argaeus) - ThermostatGUIController/Frontend for a room thermostat with epaper
 * [Archippe](https://gitlab.com/pelops/archippe) - Archippe is a data persistence micro service for pelops. Targets are influxdb and csv-files. 
 * [Copreus](https://gitlab.com/pelops/copreus) - This library provides a framework to write device driver for the raspberry pi that are connected to MQTT.
 * [Epidaurus](https://gitlab.com/pelops/epidaurus) - PID controller for thermostat
 * [Eurydike](https://gitlab.com/pelops/eurydike) - Eurydike is a simple event detection. Reacts to above-threshold, below-threshold, and outside value-band.  
 * [Hippasos](https://gitlab.com/pelops/hippasos) - Mqtt microservice to play sounds.  
 * [Nikippe](https://gitlab.com/pelops/nikippe) - A general purpose gui image generator/display server - takes values from mqtt and sends image to mqtt.

In production are:
 * [Lysidike](https://gitlab.com/pelops/lysidike) - Lysidike publishes incoming mqtt messages to various internet services like email. (todos: documentation)
 * [Thyestes](https://gitlab.com/pelops/thyestes) - Timer microservice. Listens on topics for specific messages, starts a timer when such a messages has been received and publishes a predefined message after the timer expired.  (todos: documentation)
 * [Skeiron](https://gitlab.com/pelops/skeiron) - Forwarding/Echo/Collect/Distribute service. (todos: documentation)
 
Planned microservices:
 * [Hippodamia](https://gitlab.com/pelops/hippodamia) - Hippodamia observe the state of all registered microservices (aka watch dog).
 * [Pleisthenes](https://gitlab.com/pelops/pleisthenes) - A weather microservice (connects to a weather site and provides e.g. local sun radiation)

Further ideas for general purpose services:
 * And/or/xor/not/nand/nor/xnor - for boolean/int messages and for arbitrary evaulation statements on the content of the messages. plus timeout (how long is a message valid to be joined with another message in such an operation)
 * Lambda - takes an incoming message, applies the configured lambda function to it, and publishes the result. three flavors: lambda code in config, python3 core function, function from an arbitrary module. important: functions must accept one parameter and one only and return one result that can be handled by the mqtt client (paho.mqtt).
 
Ideas for controllers / applications:
 * A pool pump / solar panel controller that heats/cools the pool 
 * A floor heating system controller
 * A multiroom humidifier controller

The project [Pelops](https://gitlab.com/pelops/pelops) provides common classes like mqtt-client, pyyaml wrapper. Thus it is not a microservice itself.

# Tutorial

  * [Step 0](https://gitlab.com/pelops/pelops/tree/master/examples/0_setup.md) - prerequisites
  * [Step 1](https://gitlab.com/pelops/pelops/tree/master/examples/1_input-output.md) - while the button is pressed, turn on the led.
  * [Step 2](https://gitlab.com/pelops/pelops/tree/master/examples/2_input-display.md) - display the button state on an ePaper
  * [Step 3](https://gitlab.com/pelops/pelops/tree/master/examples/3_temperature-threshold-output.md) - if the temperature readings (update regularly) from a DHT22 are above a threshold, turn on the led.
  * [Step 4](https://gitlab.com/pelops/pelops/tree/master/examples/4_temperature-calibration.md) - calibrate the temperature sensor
  * [Step 5](https://gitlab.com/pelops/pelops/tree/master/examples/5_temperature-on-demand.md) - measure temperature every time the button has been pressed 
  * [Step 6](https://gitlab.com/pelops/pelops/tree/master/examples/6_temperature-display.md) - display temperature sensor readings on an ePaper (same raspi)
  * [Step 7](https://gitlab.com/pelops/pelops/tree/master/examples/7_display-activity-led.md) - use the led in the setup to show if a display update is pending.
  * [Step 8](https://gitlab.com/pelops/pelops/tree/master/examples/8_temperature-remote-display.md) - display temperature sensor readings on an ePaper that is connected to another raspi
  * [Step 9](https://gitlab.com/pelops/pelops/tree/master/examples/9_two-sites.md) - use AWS IoT to bridge between one site where the temperature is measured and 
  another site where it is displayed on an ePaper
  
 
  * Display DHT22 sensor readings on an ePaper [...](https://gitlab.com/pelops/pelops/tree/master/examples/display_temperature.md)

# Examples
 
Planned examples:
  * A rich room temperature controller

# Modules

Pelops is a good father and provides tools for all his children.

## AbstractMicroservice
Base class for all MicroServices of pelops. Takes care of reading and validating the config, providing mymqttclient
and logger instances as well as static methods to create an instance and run it indefinitly.

If no mqtt client has been provided, the config must have an "mqtt" entry at root level. Same accounts for the
logger.

An implementation of this abstract class should use the provided config, mqtt_client, and logger. But most
importantly, it must adhere to the _is_stopped and _stop_service Events and make good use of the _start and
_stop methods. Otherwise, starting and stopping the microservice might not be possible in the framework.

The two events/flags _is_started and _is_stopped show the state of the Service. They are changed in the methods
start and stop. During the start and the stopped sequences, both events are cleared. Thus, in case of an error
during these sequences, the state of the microservice is undefined.


## MyConfigTools
Set of scripts for yaml/json configfile reading.

  * ```read_config```:
This method reads the provided file, converts it to a yaml config structure, expands the credential file entries 
(e.g. for mqtt and influx db) and makes sure the keys are lower case. Credential files are yaml files themselves and are merged by searching for all keys that are equivalent to the 
specified string (e.g. "credential-file"). Every value of these entries is assumed to be a valid file name - a config 
yaml file containing credentials. These files a read, parsed and merged into the general config structure.

  * ```validate_config```: Validate the provided config with the provided schema.
  
  * ```deep_update```: Merge a yaml struct (=extensions) into another yaml struct (=base). List entries yield a 
TypeError (except if the list is already in a new subtree that is not present in base at all). As this merge method 
advances only to subtrees in base if this subtree exists in the extensions as well, existing lists in base will 
never be visited.

  * ```dict_deepcopy_lowercase```: Convert all keys in the dict (and sub-dicts and sub-dicts of sub-lists) to lower case. Returns a deep copy of the 
original dict.

## MyMQTTCLient

Wrapper for the paho.mqtt.client. Provides a topic to method mapping, thus enabling that one instance of
paho.mqtt.client can be used with different incoming message handler. Further, it separates the time of
registering a subscription from the status of the connection. Subscribed topic/handler pairs are automatically
registered / unregistered upon connection/disconnection.

## HistoryAgent
Takes provided data, aggregates it and stores it locally up to the defined history length. Optionally, fetches old 
data from dataservice like archippe.
  
## ImageMQTTMessageConverter
Static utility class - converts images and json structures into valid mqtt payloads.
 
 * ```to_full_image_message```: Convert a PIL.Image instance to bytes - the format nedded if the mqtt payload consists 
 of only the image.
 * ```to_partial_images_message```: Takes a list containing [x,y,partial images] and converts the images into an utf-8 
 encoded string that can be accepted by mqtt and packs them into a json structure consisting of these string and their 
 x/y values.
  
 
  
  