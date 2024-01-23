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
            config = yaml.safe_load(file)
            config['hiit'] = {
                'age': config.get('hiit_age', -1),
                'min_percentage': config.get('hiit_min_percentage', 60),
                'max_percentage': config.get('hiit_max_percentage', 90),
                'high_phase_duration': config.get('hiit_high_phase_duration', 3),  # in minutes
                'low_phase_duration': config.get('hiit_low_phase_duration', 2),
                'cycles': config.get('hiit_cycles', 3)
            }
            return config

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
    target_bpm = config.get('target_bpm', -1)
    error_margin = config.get('error_margin', -1)
    hiit_config = config.get('hiit', None)

    ble_device_manager = None
    heart_rate_monitor = None

    if ble_device_address != "default_address":
        print(f"Using BLE device address from configuration file: {ble_device_address}")
        ble_device_manager = BLEDeviceManager(ble_device_address)
    else:
        print("No BLE device address specified in configuration file.")
        print("Please specify the BLE device address in the configuration file.")
        exit()

    if target_bpm != -1 and error_margin != -1 and hiit_config['age'] != -1:
        print(f"Using target bpm from configuration file: {target_bpm} bpm +/- {error_margin} bpm and age {hiit_config['age']}")
        heart_rate_monitor = HeartRateMonitor(loop, ble_device_manager, target_bpm, error_margin, hiit_config)
    else:
        print("No steady state target zone or age specified in configuration file.")
        print("Please specify the target zone in the configuration file.")
        exit()
    
    app = GUI(loop, heart_rate_monitor)
    heart_rate_monitor.register_observer(app)

    app.after(0, run_asyncio_iteration, loop)
    app.mainloop()
