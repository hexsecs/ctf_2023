import can
import time

def send_iso_tp_message(arbitration_id, data, channel):
    message = can.Message(arbitration_id=arbitration_id, data=data)
    channel.send(message)

def increment_address(address, request_size):
    address_int = int(address, 16)
    request_int = int(request_size.replace(' ', ''), 16)
    incremented_address = address_int + request_int
    return format(incremented_address, '08X')

def main():

# Define the start address and request size
    start_address = "C3F80000"
    end_address = "c3ffffff"
    request_size = "08"

# Create a CAN bus instance
    bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)

# Iterate through the address space and send ISO-TP messages
    while int(start_address.replace(' ', ''), 16) <= int("C3FFFFFF", 16):
# Prepare the data to be sent (8-byte request)
        data = bytes.fromhex(start_address.replace(' ', '') + request_size.replace(' ', ''))
        print(data)

        # Send the ISO-TP message
        send_iso_tp_message(arbitration_id=0x7e0, data=data, channel=bus)

        # Add a delay if needed between each message to avoid flooding the bus
        # time.sleep(0.1)

        # Increment the address
        start_address = increment_address(start_address, request_size)


if __name__ == "__main__":
    main()
