# MicroPython-RFID-Lock
A door lock system using RFID keys running on an ESP32 client and an ESP32 server.
This isn't the most generic code written. The bulk of it will be the `doorunlock.py` file, which contains both a client and server class that can be instantiated separately. In the examples folder, the `boot.py` and `main.py` files that would be needed on the client and server are reproduced for reference. 

# Hardware used
 * Adafruit's HUZZAH32 ESP32 board, for client ([link](https://www.adafruit.com/product/3405))
 * Adafruit's NeoPixel FeatherWing - 4x8 RGB LED matrix, for client (I already had this available, but could be swapped with any LED indicator, or omitted entirely) ([link](https://www.adafruit.com/product/2945))
 * Generic ESP32 board from aliexpress, for server
 
# Software used
 * MicroPython firmware for ESP32. v1.10, 2019-01-25 build. ([link](http://micropython.org/resources/firmware/esp32-20190125-v1.10.bin))
