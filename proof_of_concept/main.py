"""
main.py

This script is used for Bluetooth Low Energy (BLE) communication with a heart rate monitor.
It uses the `bleak` library to scan for BLE devices, connect to a specific device, and read heart rate data.

Note: The heart rate is read from a standard Heart Rate service with the UUID "00002a37-0000-1000-8000-00805f9b34fb".
"""

# Step 1: Import Libraries
# We're using the `bleak` library for BLE communication.
from bleak import BleakScanner, BleakClient
import asyncio
import yaml
import os

# Step 2: Scan for Devices
# This function will scan for BLE devices and print them out.
async def scan_for_devices():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device found: {device.name}, Address: {device.address}")
    return devices

# Step 3: Connect to a Device
# This function will attempt to connect to the device with the given address.
async def connect_to_device(address):
    print(f"Connecting to BLE device at address {address}")
    client = BleakClient(address)
    try:
        await client.connect()
        print(f"Connected to {address}")
        return client
    except Exception as e:
        print(f"Could not connect to the device: {e}")
        return None

# Step 4: Read Heart Rate
# This function reads the heart rate from the connected device.
async def read_heart_rate(client):
    HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"  # Standard Heart Rate service UUID

    def notification_handler(sender, data):
        flags = data[0]
        is_16bit = flags & 1
        heart_rate = int.from_bytes(data[1:3] if is_16bit else data[1:2], byteorder='little')
        print(f"Heart Rate: {heart_rate} bpm")


    print("Subscribing to heart rate notifications...")
    await client.start_notify(HEART_RATE_UUID, notification_handler)
    await asyncio.sleep(30)  # Keep the script running for 30 seconds to receive notifications
    await client.stop_notify(HEART_RATE_UUID)

# Step 5: Get MAC Address from Config File
# This function reads the MAC address from the 'mac' field of the yaml config file.
async def get_mac_address():
    config_file_path = "config.yaml"
    
    if not os.path.exists(config_file_path):
        # Prompt the user to add a MAC address in the config file
        mac_address = input("Please enter the MAC address: ")
        
        # Create the config file and write the MAC address
        with open(config_file_path, "w") as config_file:
            config_file.write(f"mac: {mac_address}")

        print("Created config file.")
        print(f"MAC address {mac_address} added to config file.")
        
        return mac_address
    
    with open(config_file_path, "r") as config_file:
        config = yaml.safe_load(config_file)
        return config["mac"]


# Step 5: Main Async Function
# This function will run the above steps.
async def main():
    # Scan for devices (optional)
    # devices = await scan_for_devices()
    
    # connect to the device with the given address in the config file
    device_address = await get_mac_address()
    client = await connect_to_device(device_address)
    
    # If we've successfully connected, read the heart rate.
    if client and client.is_connected:
        await read_heart_rate(client)
        
        # Disconnect from the client
        await client.disconnect()
        print(f"Disconnected from {device_address}")

# Step 6: Run the Main Function
# This will start the async event loop and run the main function.
# Instead of:
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

# Use:
asyncio.run(main())