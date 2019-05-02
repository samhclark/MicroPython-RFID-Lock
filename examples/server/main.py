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

from usocket import socket, AF_INET, SOCK_STREAM
import doorunlock

#-----------------------------------------------------------------------------#
# Initializations                                                             #
#-----------------------------------------------------------------------------#

ssid =  # your ssid here, as a string
pw =  # your password here, as a string
wlan = connect_wifi(ssid, pw)
server_address = (wlan.ifconfig()[0], int(8696))
this_socket = socket(AF_INET, SOCK_STREAM)
this_socket.bind(server_address)
this_socket.listen(3)

# If this code would be deployed on the ESP32, the salt, key, and
# iv should be baked in to the firmware and deployed that way
AES_256_CBC_KEY =  # put your AES key here
AES_256_CBC_IV =  # put your AES IV here
AES_256_CBC_SALT =  # put your AES salt here

valid_hash_list =  # put a list of valid hashes here

du = doorunlock.RFIDDoorUnlockServer(this_socket, AES_256_CBC_KEY, AES_256_CBC_IV, valid_hash_list)


print("REPL Starting")


#-----------------------------------------------------------------------------#
# End of main.py                                                              #
#-----------------------------------------------------------------------------#
