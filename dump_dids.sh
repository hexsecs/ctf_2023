#!/bin/ash

# Define the range of addresses (from 0xC3F80000 to 0xC3FFFFFF)
start_did=$((0x0000))
end_did=$((0xFFFF))
did=$start_did

while [ $did -le $end_did ]
do
    # Convert the address to hexadecimal and pad it to 8 characters
    hex_did=$(printf "%04X" $did)

    # Prepare the data to be sent (8-byte request)
    data="22 $hex_did"
    data=${data// /}

    # Use sed to insert a space after every two characters
    formatted_string=$(echo "$data" | sed -E 's/(..)/\1 /g')

    echo "$formatted_string"

    # Send the ISO-TP message
    echo "$formatted_string" | isotpsend -s 7e0 -d 7e8 vcan0


    # Add a delay if needed between each message to avoid flooding the bus
    # sleep 0.1

    # Increment the address
    did=$(($did + 1))
done

