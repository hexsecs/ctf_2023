#!/bin/ash

# Send the ISO-TP message
echo "11 01" | isotpsend -s 7e0 -d 7e8 vcan0
