import asyncio
import yaml
from tkinter import Tk
from BLEDeviceManager import BLEDeviceManager
from HeartRateMonitor import HeartRateMonitor
from GUI import GUI
import os

def load_configuration(file_path='config.yaml'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    else:
        print(f"Configuration file '{file_path}' does not exist.")
        return None

def run_asyncio_iteration(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()
    app.after(10, run_asyncio_iteration, loop)

if __name__ == "__main__":
    config = load_configuration()

    loop = asyncio.get_event_loop()

    ble_device_address = config.get('ble_device_address', 'default_address')
    target_zone = config.get('target_zone', {'lower': 0, 'upper': 300})

    ble_device_manager = None
    heart_rate_monitor = None

    if ble_device_address != "default_address":
        print(f"Using BLE device address from configuration file: {ble_device_address}")
        ble_device_manager = BLEDeviceManager(ble_device_address)
    else:
        print("No BLE device address specified in configuration file.")
        print("Please specify the BLE device address in the configuration file.")
        exit()

    if target_zone != {'lower': 0, 'upper': 300}:
        print(f"Using target zone from configuration file: {target_zone}")
        heart_rate_monitor = HeartRateMonitor(ble_device_manager, (target_zone['lower'], target_zone['upper']))
    else:
        print("No target zone specified in configuration file.")
        print("Please specify the target zone in the configuration file.")
        exit()
    
    app = GUI(loop, heart_rate_monitor)
    heart_rate_monitor.register_observer(app)

    app.after(0, run_asyncio_iteration, loop)
    app.mainloop()
