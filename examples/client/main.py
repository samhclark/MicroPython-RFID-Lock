# California State University, Fresno
# Electrical and Computer Engineering Department
# ECE 122L - Digital Systems Lab - Spring 2019
# Instructor: Dr. Reza Raeisi
# Author: Sam Clark

# Skeleton main.py file
# This file is executed on every boot (including wake-boot from deepsleep)
# This file is executed after boot.py

#-----------------------------------------------------------------------------#
# Import statements                                                           #
#-----------------------------------------------------------------------------#

from machine import Pin, SPI
from umqtt.simple import MQTTClient  # For server communication
import mfrc522  # RFID reader library
import doorunlock

#-----------------------------------------------------------------------------#
# Initializations                                                             #
#-----------------------------------------------------------------------------#

ssid = 'yourssid'
pw = 'yourpassword'
wlan = connect_wifi(ssid, pw)

room_number = '281'

SCK = Pin(18, Pin.OUT)
MOSI = Pin(23, Pin.OUT)
MISO = Pin(19, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=SCK, mosi=MOSI, miso=MISO)
SDA = Pin(5, Pin.OUT)
mfrc_rdr = mfrc522.MFRC522(spi, SDA)

your_server_address =  # your IPv4 address here, as a string
your_server_port =  # your port here, as an int
server_address = (your_server_address, your_server_port)

your_mqtt_broker_addr =  # your MQTT broker IPv4 address, as a string
mqtt_client = MQTTClient(bytes('rfid-'+room_number,'utf-8'),your_mqtt_broker_addr, port=1883)

# If this code would be deployed on the ESP32, the salt, key, and
# iv should be baked in to the firmware and deployed that way so at least it isnt
# in plain text in your source code
AES_256_CBC_KEY =  # put your AES key here
AES_256_CBC_IV =  # put yout AES IV here
AES_256_CBC_SALT =  # put your AES salt here (not used)

du = doorunlock.RFIDDoorUnlockClient(room_number, mfrc_rdr, server_address, mqtt_client, AES_256_CBC_KEY, AES_256_CBC_IV)


print("REPL Starting")


#-----------------------------------------------------------------------------#
# End of main.py                                                              #
#-----------------------------------------------------------------------------#
