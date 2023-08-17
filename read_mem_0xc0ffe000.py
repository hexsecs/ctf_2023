import can
import random
import struct
import time
import binascii
#import uds
#from uds import Uds

ECU_ID = 0x7E0
TOOL_ID = 0x7E8
seed = [0,0, 0, 0]
key = [0,0, 0, 0]

def request_seed(bus):
    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x27, 0x01], is_extended_id=False)
    bus.send(msg)

    while True:
        response = bus.recv(1)
        if response is not None and response.arbitration_id == TOOL_ID:
            print(response)
            if response.data[1] == 0x67:
                seed[0] = response.data[3] 
                seed[1] = response.data[4] 
                seed[2] = response.data[5] 
                seed[3] = response.data[6] 
                for value in seed:
                    print(hex(value))
                return seed

def generate_key(seed, xor_value):
    for i in range(4):
        key[i] = seed[i] ^ xor_value
        print(hex(key[i]))
    return key 

def send_key(bus, key):
    msg = can.Message(arbitration_id=ECU_ID, data=[0x04, 0x27, 0x02] + list(key), is_extended_id=False)
    bus.send(msg)

    while True:
        response = bus.recv(1)
        if response is not None and response.arbitration_id == TOOL_ID:
            if response.data[1] == 0x67 and response.data[2] == 0x04:
                return True
        return False

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
#    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x11, 0x01], is_extended_id=False)
#    bus.send(msg)
#    time.sleep(2)
#
#    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x10, 0x03], is_extended_id=False)
#    bus.send(msg)
#    time.sleep(0.5)

#    seed = request_seed(bus)
#    print(f"Seed: {seed}")
#
#    key = generate_key(seed, 0xff)
#    print(f"Generated Key: {key}")
#
#    if send_key(bus, key):
#        print("Unlocked Security Access Level 3")
#        time.sleep(0.5)
#
#    else:
#        print("Key is invalid")
#        quit()

    print("Going to session 2")
    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x10, 0x02], is_extended_id=False)
    bus.send(msg)

    while True:
        response = bus.recv(1)
        if response is not None and response.arbitration_id == TOOL_ID:
            print(response)
            if response.data[1] == 0x50 and response.data[2] == 0x02:
                break


    start_address = 0xc0ffe000
    end_address = 0xc0ffffff 

    for address in range(start_address, end_address + 1, 0x08):  # Increment by 0x80 
        time.sleep(0.1)
        byte3 = (address & 0xFF000000) >> 24 
        byte2 = (address & 0x00FF0000) >> 16
        byte1 = (address & 0x0000FF00) >> 8 
        byte0 = (address & 0x000000FF) 

        data = [0x07, 0x23, 0x14, byte3, byte2, byte1, byte0, 0x08] 
        msg = can.Message(arbitration_id=ECU_ID, data=data, is_extended_id=False)
        bus.send(msg)

        while True:
            response = bus.recv(1)
            print(response)
            if response is not None and response.arbitration_id == TOOL_ID:
                if response.data[1] == 0x63:
                    break
                if response.data[0] == 0x10 and response.data[2] == 0x63:
                    msg = can.Message(arbitration_id=ECU_ID, data=[0x30, 0x00, 0x00], is_extended_id=False)
                    bus.send(msg)
                    break
                if response.data[1] == 0x7f:
                    break


    print("Going to session 1")

    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x10, 0x01], is_extended_id=False)
    bus.send(msg)

    print("here")
    while True:
        response = bus.recv(1)
        if response is not None and response.arbitration_id == TOOL_ID:
            print(response)
            if response.data[1] == 0x50 and response.data[2] == 0x01:
                break


    start_address = 0xc0ffe000
    end_address = 0xc0ffffff 

    for address in range(start_address, end_address + 1, 0x08):  # Increment by 0x80 
        time.sleep(0.1)
        byte3 = (address & 0xFF000000) >> 24 
        byte2 = (address & 0x00FF0000) >> 16
        byte1 = (address & 0x0000FF00) >> 8 
        byte0 = (address & 0x000000FF) 

        data = [0x07, 0x23, 0x14, byte3, byte2, byte1, byte0, 0x08] 
        msg = can.Message(arbitration_id=ECU_ID, data=data, is_extended_id=False)
        bus.send(msg)

        while True:
            response = bus.recv(1)
            print(response)
            if response is not None and response.arbitration_id == TOOL_ID:
                if response.data[1] == 0x63:
                    break
                if response.data[0] == 0x10 and response.data[2] == 0x63:
                    msg = can.Message(arbitration_id=ECU_ID, data=[0x30, 0x00, 0x00], is_extended_id=False)
                    bus.send(msg)
                    break
                if response.data[1] == 0x7f:
                    break

    # Trying in session 3
    print("Going to session 3")

    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x10, 0x03], is_extended_id=False)
    bus.send(msg)

    print("here")
    while True:
        response = bus.recv(1)
        if response is not None and response.arbitration_id == TOOL_ID:
            print(response)
            if response.data[1] == 0x50 and response.data[2] == 0x03:
                break


#    seed = request_seed(bus)
#    print(f"Seed: {seed}")
#
#    key = generate_key(seed, 0x20)
#    print(f"Generated Key: {key}")
#
#    if send_key(bus, key):
#        print("Unlocked Security Access Level 3")
#        time.sleep(0.5)
#
#    else:
#        print("Key is invalid")
#        quit()

    start_address = 0xc0ffe000
    end_address = 0xc0ffffff 

    for address in range(start_address, end_address + 1, 0x08):  # Increment by 0x80 
        time.sleep(0.1)
        byte3 = (address & 0xFF000000) >> 24 
        byte2 = (address & 0x00FF0000) >> 16
        byte1 = (address & 0x0000FF00) >> 8 
        byte0 = (address & 0x000000FF) 

        data = [0x07, 0x23, 0x14, byte3, byte2, byte1, byte0, 0x08] 
        msg = can.Message(arbitration_id=ECU_ID, data=data, is_extended_id=False)
        bus.send(msg)

        while True:
            response = bus.recv(1)
            print(response)
            if response is not None and response.arbitration_id == TOOL_ID:
                if response.data[1] == 0x63:
                    break
                if response.data[0] == 0x10 and response.data[2] == 0x63:
                    msg = can.Message(arbitration_id=ECU_ID, data=[0x30, 0x00, 0x00], is_extended_id=False)
                    bus.send(msg)
                    break
                if response.data[1] == 0x7f:
                    break
if __name__ == "__main__":
    main()


