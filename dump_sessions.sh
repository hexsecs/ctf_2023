#!/bin/ash

# Define the range of session IDs from 0x00 to 0xFF
start_session=$((0x00))
end_session=$((0xFF))
session=$start_session

while [ $session -le $end_session ]
do
    # Convert the address to hexadecimal and pad it to 8 characters
    hex_session=$(printf "%02X" $session)

    # Prepare the data to be sent (8-byte request)
    data="10 $hex_session"
    data=${data// /}

    # Use sed to insert a space after every two characters
    formatted_string=$(echo "$data" | sed -E 's/(..)/\1 /g')

    echo "$formatted_string"

    # Send the ISO-TP message
    echo "$formatted_string" | isotpsend -s 7e0 -d 7e8 vcan0


    # Add a delay if needed between each message to avoid flooding the bus
    # sleep 0.1

    # Increment the address
    session=$(($session + 1))
done

