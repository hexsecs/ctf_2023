#!/bin/ash

# Go to programming session
formatted_string="10 02"
echo "$formatted_string" | isotpsend -s 7e0 -d 7e8 vcan0

# Define the range of addresses (from 0xC3F80000 to 0xC3FFFFFF)
start_address=$((0x01a000))
end_address=$((0xFFFFFF))
address=$start_address

while [ $address -le $end_address ]
do
    # Convert the address to hexadecimal and pad it to 8 characters
    hex_address=$(printf "%08X" $address)

    # Prepare the data to be sent (8-byte request)
    data="23 14 $hex_address 20"
    data=${data// /}

    # Use sed to insert a space after every two characters
    formatted_string=$(echo "$data" | sed -E 's/(..)/\1 /g')

    #echo "$formatted_hex" 
    echo "$formatted_string"

    # Send the ISO-TP message
    echo "$formatted_string" | isotpsend -s 7e0 -d 7e8 vcan0


    # Add a delay if needed between each message to avoid flooding the bus
     sleep 1 

    # Increment the address
    address=$(($address + 0x20 ))
done

