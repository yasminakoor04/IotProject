import ubinascii        # Conversions between binary data and various encodings
import machine          # To Generate a unique id from processor

# Wireless network
WIFI_SSID = "JayZ-7"
WIFI_PASS = 'Ilovecoffee23'   # No this is not our regular password. :)

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "Yasminakoor"
AIO_KEY = "aio_MaGz98qUvFoNlyVu27k1n0smBwhl"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
AIO_HUMIDITY_FEED = "Yasminakoor/feeds/humidity"
AIO_TEMPERATURE_FEED = "Yasminakoor/feeds/temperature"
AIO_TILT_FEED = "Yasminakoor/feeds/tilt"
