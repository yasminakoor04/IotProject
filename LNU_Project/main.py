import dht
import machine
import time
from wifiConnection import connect, disconnect
from mqtt import MQTTClient   # Import MQTTClient from your mqtt module
import keys                   # Import keys module for configuration

# Connect to Wi-Fi
ip = connect()

# Check if the connection was successful
if ip:
    print('Wi-Fi connected successfully! IP:', ip)
else:
    print('Wi-Fi connection failed.')
    raise Exception("Wi-Fi connection failed. Exiting...")

# Initialize DHT11 sensor on GPIO 22
dhtSensor = dht.DHT11(machine.Pin(22))

# Tilt switch setup on GPIO 27 with pull-up resistor
tiltPin = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

# LED setup on GPIO 10
ledPin = machine.Pin(10, machine.Pin.OUT)

# Initialize MQTT client
client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)

try:
    # Connect to Adafruit IO MQTT server
    client.connect()
    print("Connected to Adafruit IO MQTT server.")

    # Main loop to read sensor data and publish periodically
    while True:
        try:
            # Read DHT sensor data
            dhtSensor.measure()
            temperature = dhtSensor.temperature()
            humidity = dhtSensor.humidity()

            # Print temperature and humidity data
            print("Temperature is {} degrees Celsius and Humidity is {}%".
                  format(temperature, humidity))

            # Read current tilt switch state
            current_tilt_state = tiltPin.value()

            # Always print the current tilt switch state
            print("Tilt switch state:", "ON" if current_tilt_state == 0 else "OFF")

            # Turn on/off the LED based on the tilt switch state
            if current_tilt_state == 0:
                ledPin.on()
            else:
                ledPin.off()

            # Print the LED state
            print("LED state:", "ON" if ledPin.value() else "OFF")

            # Publish the tilt state and sensor data to Adafruit IO
            client.publish(topic=keys.AIO_TILT_FEED, msg="ON" if current_tilt_state == 0 else "OFF")
            client.publish(topic=keys.AIO_TEMPERATURE_FEED, msg=str(temperature))
            client.publish(topic=keys.AIO_HUMIDITY_FEED, msg=str(humidity))

            # Sleep for 2 seconds before the next loop
            time.sleep(2)

        except Exception as e:
            print("Exception occurred in main loop:", e)
            time.sleep(2)

except KeyboardInterrupt:
    print('Terminating the program.')

finally:
    # Disconnect MQTT client
    client.disconnect()
    print("Disconnected from Adafruit IO MQTT server.")

    # Disconnect from Wi-Fi
    disconnect()
    print("Disconnected from Wi-Fi.")
