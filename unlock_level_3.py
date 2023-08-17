import can
import random
import struct
import time
import binascii
#import uds
#from uds import Uds

ECU_ID = 0x7E0
TOOL_ID = 0x7E8
seed = [0,0]
key = [0,0]

def request_seed(bus):
    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x27, 0x03], is_extended_id=False)
    bus.send(msg)

    while True:
        response = bus.recv(1)
        if response is not None and response.arbitration_id == TOOL_ID:
            print(response)
            if response.data[1] == 0x67:
                seed[0] = response.data[3] 
                seed[1] = response.data[4] 
                for value in seed:
                    print(hex(value))
                return seed

def generate_key(seed, xor_value):
    for i in range(2):
        key[i] = seed[i] ^ xor_value
        print(hex(key[i]))
    return key 

def send_key(bus, key):
    msg = can.Message(arbitration_id=ECU_ID, data=[0x04, 0x27, 0x04] + list(key), is_extended_id=False)
    bus.send(msg)

    while True:
        response = bus.recv(1)
        if response is not None and response.arbitration_id == TOOL_ID:
            if response.data[1] == 0x67 and response.data[2] == 0x04:
                return True
        return False

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x11, 0x01], is_extended_id=False)
    bus.send(msg)
    time.sleep(2)

    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x10, 0x03], is_extended_id=False)
    bus.send(msg)
    time.sleep(0.5)

    seed = request_seed(bus)
    print(f"Seed: {seed}")

    key = generate_key(seed, 0xff)
    print(f"Generated Key: {key}")

    if send_key(bus, key):
        print("Unlocked Security Access Level 3")
        time.sleep(0.5)

    else:
        print("Key is invalid")

if __name__ == "__main__":
    main()


