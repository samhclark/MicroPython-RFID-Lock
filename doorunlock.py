# California State University, Fresno
# Electrical and Computer Engineering Department
# ECE 122L - Digital Systems Lab - Spring 2019
# Instructor: Dr. Reza Raeisi
# Author: Sam Clark
# RFID Room Reader class file

#-----------------------------------------------------------------------------#
# Import statements                                                           #
#-----------------------------------------------------------------------------#
from uos import urandom
from time import sleep_ms
from uhashlib import sha256
from ucryptolib import aes
from usocket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from machine import Pin
from neopixel import NeoPixel  # Remove if not using the NeoPixel
import _thread

#-----------------------------------------------------------------------------#
# Class Definition                                                            #
#-----------------------------------------------------------------------------#
class RFIDDoorUnlockClient:
    """Client class. Interacts directly with the MFRC522 RFID reader."""

    def __init__(self, room_num, mfrc_reader, remote_addr, mqtt_obj, aes_key, aes_iv):
        self.room = room_num
        self.rdr = mfrc_reader
        self.server_addr = remote_addr
        self.mqtt = mqtt_obj
        self.__key = aes_key
        self.__iv = aes_iv
        # Only using the neopixel instance for showing visually if the RFID tag was valid
        self.np = NeoPixel(Pin(17,Pin.OUT),32)
        print("RFID Door Unlock Client created")
        self.__running_thread = _thread.start_new_thread(self.run, tuple())

    def __str__(self):
        return ("Room: " + self.room + ", Verification Server: "
                + self.server_addr[0] + ":" + self.server_addr[1]
                + "\nAES 256 CBC Key: " + str(self.__key)
                + "\nAES 256 CBC IV: " + str(self.__iv))

    def __repr__(self):
        return (self.room, repr(self.rdr), self.server_addr,
                repr(self.mqtt), self.__key, self.__iv)

    # TODO: Implement __del__ method as soon as MicroPython supports it
    # for user created classes

    def run(self):
        """Constantly running on a thread once the instance is created

        Based heavily off of the do_read method from Tasmi Devil's
        MFRC522 examples.
        """
        while True:
            sleep_ms(100)  # Small lag for the RFID reader
            uid_hash = ''
            (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)
            if stat == self.rdr.OK:
                print("reader status OK")
                (stat, raw_uid) = self.rdr.anticoll()
                if stat == self.rdr.OK:
                    print("reader status OK after anticoll")
                    h = sha256()
                    h.update(bytes(raw_uid))
                    uid_hash = h.digest()
                    print("RFID tag UID SHA-256 hash:")
                    print(uid_hash)
                    secure_packet, n = self.make_secure_packet(uid_hash)
                    print("Secure packet created")
                    client = socket(AF_INET, SOCK_STREAM)
                    client.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                    client.connect(self.server_addr)
                    print("Connected to server")
                    client.sendall(secure_packet)  # 64-byte packet
                    print("Sent secure packet to server")
                    # TODO: set up a timeout here. Only wait for so long
                    response = client.recv(64)
                    print("Received response from server")
                    try:
                        client.close()
                        del client
                        print("Disconnected from server")
                    except AttributeError:
                        print("Connection closed on server side")
                    if self.verify(response, n):
                        print("Passed verification")
                        self.unlock_door()
                    else:
                        print("Failed verification")
                        self.blink_fail_lights()

    def make_secure_packet(self, h):
        """Encrypts and returns plaintext appended with a 32B nonce (also returned)

        AES 256 CBC is used (as opposed to EBC which would not be secure
        in this implementation)
        """
        nonce = urandom(32)
        plaintext = h + nonce
        e = aes(self.__key, 2, self.__iv)
        print("AES encrypter created")
        return e.encrypt(plaintext), nonce

    def verify(self, pkt, n):
        """Verifies the packet received has the same nonce as the one sent"""
        d = aes(self.__key, 2, self.__iv)
        plaintext = d.decrypt(pkt)
        payload = plaintext[:32]
        nonce = plaintext[32:]
        if n == nonce:
            print("Valid nonce")
            h = sha256()
            h.update(b'valid')  # the string that is hashed on the server side
            if payload == h.digest():
                print("Valid payload")
                return True
        return False

    def unlock_door(self):
        """Handles whatever things must be done to unlock the door

        In the specific version used for this project, this means
          1: Publishing the unlocked status to the MQTT broker
          2: Turning on the green LEDs
          3: Physically unlocking the door
          4: Waiting 5 seconds
          5: Physically locking the door
          6: Turning off the LEDs
          7: Publishing the locked status to the MQTT broker
        """
        #self.mqtt.connect()
        #print("Connected to MQTT broker")
        #self.mqtt.publish('/'+self.room_num+'/lock', 'unlocked')
        #print("'unlocked' sent to MQTT broker")
        #self.mqtt.disconnect()
        #print("Disconnected from MQTT broker")
        self.np.fill((0,10,0))
        self.np.write()
        # TODO: Physically unlock the door
        sleep_ms(5000)
        # TODO: Physically lock the door
        self.np.fill((0,0,0))
        self.np.write()
        #self.mqtt.connect()
        #print("Connected to MQTT broker")
        #self.mqtt.publish('/'+self.room_num+'/lock', 'locked')
        #print("'locked' sent to MQTT broker")
        #self.mqtt.disconnect()
        #print("Disconnected from MQTT broker")
        return

    def blink_fail_lights(self):
        """Blink the light pattern for a failed verification"""
        self.np.fill((10,0,0))
        self.np.write()
        sleep_ms(100)
        self.np.fill((0,0,0))
        self.np.write()
        sleep_ms(100)
        self.np.fill((10,0,0))
        self.np.write()
        sleep_ms(100)
        self.np.fill((0,0,0))
        self.np.write()
        sleep_ms(100)
        self.np.fill((10,0,0))
        self.np.write()
        sleep_ms(100)
        self.np.fill((0,0,0))
        self.np.write()
        sleep_ms(1000)


class RFIDDoorUnlockServer:
    """Server class.

    Ideally this shouldn't run on an ESP32.
    """
    def __init__(self,
                 server_socket_obj,
                 aes_key,
                 aes_iv,
                 valid_hash_list):
        self.server = server_socket_obj
        self.__key = aes_key
        self.__iv = aes_iv
        self.__valid_hashes = valid_hash_list
        print("RFID Door Unlock Server created successfully")
        self.__running_thread = _thread.start_new_thread(self.accept_incoming_connections,
                                                         (self.server,))

    def __str__(self):
        return ("Server info: " + str(self.server)
                + "\nAES 256 CBC Key: " + str(self.__key)
                + "\nAES 256 CBC IV: " + str(self.__iv)
                + "\nValid hashes: " + str(self.__valid_hashes)

    def __repr__(self):
        return (repr(self.server), self.__key, self.__iv, self.__valid_hashes)

    # TODO: Implement __del__ method as soon as MicroPython supports it
    # for user created classes

    def accept_incoming_connections(self, thisSocket):
        """
        Accept and handle incoming socket connections
        Takes the server's socket as an argument
        """
        while 1:
            # Accept incoming connections to this server
            # client:       a new socket object
            # client_addr:  the address bound to that socket
            print("Waiting for new connection...")
            client, client_addr = thisSocket.accept()
            print("Connection received")
            # The server will receive a 64 Byte payload. The first 32 bytes are the
            # SHA-256 hash of the RFID tag that was read. The second 32 bytes are
            # a nonce from the other device that must be returned to prevent replay
            ciphertext = client.recv(64)
            print("Received data from client")
            d = aes(self.__key, 2, self.__iv)
            plaintext = d.decrypt(ciphertext)
            payload = plaintext[:32]
            nonce = plaintext[32:]
            h = sha256()
            if payload in self.__valid_hashes:
                print("Valid payload")
                h.update(b'valid')
            else:
                print("Invalid payload")
                h.update(b'invalid')
            response = h.digest()
            e = aes(self.__key, 2, self.__iv)
            sec_pkt = e.encrypt(response + nonce)
            client.sendall(sec_pkt)
            print("Secure packet sent to client")
            #client.close()
            #print("Connection with client ended")
            del client
            del client_addr
