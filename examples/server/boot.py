# California State University, Fresno
# Electrical and Computer Engineering Department
# ECE 122L - Digital Systems Lab - Spring 2019
# Instructor: Dr. Reza Raeisi
# Author: Sam Clark

# Skeleton boot.py file
# This file is executed on every boot (including wake-boot from deepsleep)


#-----------------------------------------------------------------------------#
# Import statements                                                           #
#-----------------------------------------------------------------------------#

#import esp
import network
#import webrepl      # uncomment this line if the webrepl has been set up


#-----------------------------------------------------------------------------#
# Initializations                                                             #
#-----------------------------------------------------------------------------#

def connect_wifi(ssid='', pwd=''):
    """Connect to a specified wifi network
    Returns the network.WLAN object
    """
    wlan = network.WLAN(network.STA_IF)

    if wlan.isconnected():                  # Let the user know if the device
        print("Debug:\tAlready connected")  # was already connected

    if not wlan.active():                   # Mark the network as active if it
        wlan.active(True)                   # is not already active

    wlan.connect(ssid,pwd)

    while not wlan.isconnected():           # Hang program execution until
        pass                                # the device is connected

    print("Debug:\tConnection to %s successful" % ssid)
    print("Debug:\tLocal IP is %s, network.WLAN object returned." % wlan.ifconfig()[0])

    return wlan


# Start the WebREPL
#webrepl.start()

#-----------------------------------------------------------------------------#
# End of boot.py                                                              #
# main.py is executed next                                                    #
#-----------------------------------------------------------------------------#
