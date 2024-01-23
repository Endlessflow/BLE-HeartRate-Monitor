import asyncio

class HeartRateMonitor:
    # Existing attributes and initializations

    def __init__(self, loop, ble_device_manager, target_bpm, error_margin, hiit_config=None):
        # Existing initialization
        self.loop = loop
        self.ble_device_manager = ble_device_manager
        self.target_bpm = target_bpm
        self.error_margin = error_margin
        self.observers = []
        self.current_heart_rate = None
        self.status = None

        # HIIT-specific attributes
        self.hiit_config = hiit_config
        self.hiit_mode_active = False
        self.hiit_phase = 'low'
        self.hiit_cycle_count = 0
        self.initial_low_target_bpm = None
        self.final_hiit_target_bpm = None
        self.current_hiit_target_bpm = None
        self.bpm_change_interval = 2  # in seconds, adjust as needed

    async def start_hiit_workout(self):
        if self.hiit_config:
            self.hiit_mode_active = True
            self.hiit_cycle_count = 0
            self.hiit_phase = 'low'
            self.max_heart_rate = (211 - 0.64 * self.hiit_config['age'])
            self.initial_low_target_bpm = self.calculate_hiit_target_bpm(self.hiit_config['min_percentage'])
            self.final_hiit_target_bpm = self.calculate_hiit_target_bpm(self.hiit_config['max_percentage'])
            self.current_hiit_target_bpm = self.initial_low_target_bpm
            self.hiit_target_bpm_increment = self.calculate_bpm_change('increase')
            self.hiit_target_bpm_decrement = self.calculate_bpm_change('decrease')
            print(f"Starting HIIT workout with {self.hiit_config['cycles']} cycles.")
            await self.update_target_bpm_periodically()
        else:
            print("No HIIT configuration provided.")

    def calculate_hiit_target_bpm(self, percentage):
        # Calculate target BPM based on the given percentage
        # Logic to calculate Max Heart Rate or get it from the config
        return int(self.max_heart_rate * percentage / 100)

    def calculate_bpm_change(self, change_type):
        if change_type == 'increase':
            total_duration = self.hiit_config['high_phase_duration'] * 60  # convert minutes to seconds
            total_change = self.final_hiit_target_bpm - self.initial_low_target_bpm
        else:  # 'decrease'
            total_duration = self.hiit_config['low_phase_duration'] * 60
            total_change = self.final_hiit_target_bpm - self.initial_low_target_bpm
        return total_change / (total_duration / self.bpm_change_interval)
    

    async def update_target_bpm_periodically(self):
        if not self.hiit_mode_active:
            return

        if self.hiit_phase == 'high':
            if self.current_hiit_target_bpm < self.final_hiit_target_bpm:
                self.current_hiit_target_bpm += self.hiit_target_bpm_increment
            else:
                # Switch to low phase after reaching high target
                self.switch_to_next_phase()

        elif self.hiit_phase == 'low':
            if self.current_hiit_target_bpm > self.initial_low_target_bpm:
                self.current_hiit_target_bpm -= self.hiit_target_bpm_decrement
            else:
                # Switch to high phase after reaching low target
                self.switch_to_next_phase()

        # Schedule the next update
        self.hiit_timer = self.loop.call_later(self.bpm_change_interval, asyncio.create_task, self.update_target_bpm_periodically())
        
    def switch_to_next_phase(self):
        if not self.hiit_mode_active:
            return

        self.hiit_phase = 'high' if self.hiit_phase == 'low' else 'low'

        if self.hiit_phase == 'high':
            self.hiit_cycle_count += 1
            if self.hiit_cycle_count >= self.hiit_config['cycles']:
                self.hiit_mode_active = False  # End HIIT workout after the last cycle
            else:
                return

    async def stop_hiit_workout(self):
        self.hiit_mode_active = False
        if self.hiit_timer:
            self.hiit_timer.cancel()
        print("HIIT workout stopped.")

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.current_heart_rate, self.status, hiit_active=self.hiit_mode_active, hiit_cycle_count=self.hiit_cycle_count, hiit_phase=self.hiit_phase, hiit_target_bpm=self.current_hiit_target_bpm)

    async def start_monitoring(self):
        if not self.ble_device_manager.is_connected():
            print("BLE device not connected. Attempting to connect...")
            await self.ble_device_manager.connect()
        print("Starting heart rate monitoring...")
        await self.subscribe_to_heart_rate()

    async def stop_monitoring(self):
        await self.unsubscribe_from_heart_rate()
        print("Stopped heart rate monitoring.")

    async def subscribe_to_heart_rate(self):
        HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

        async def notification_handler(sender, data):
            self.process_heart_rate(data)

        await self.ble_device_manager.client.start_notify(HEART_RATE_UUID, notification_handler)

    async def unsubscribe_from_heart_rate(self):
        HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
        await self.ble_device_manager.client.stop_notify(HEART_RATE_UUID)

    def change_target_bpm(self, new_target_bpm):
        self.target_bpm = new_target_bpm

    def process_heart_rate(self, data):
        flags = data[0]
        is_16bit = flags & 1
        heart_rate = int.from_bytes(data[1:3] if is_16bit else data[1:2], byteorder='little')
        print(f"Heart Rate: {heart_rate} bpm")
        self.current_heart_rate = heart_rate
        self.status = self.in_target_zone(heart_rate)
        self.notify_observers()

    def in_target_zone(self, heart_rate):
        if not self.hiit_mode_active:
            lower = self.target_bpm - self.error_margin
            upper = self.target_bpm + self.error_margin
            if heart_rate < lower:
                return "below"
            elif heart_rate > upper:
                return "above"
            else:
                return "within"
        elif self.hiit_mode_active:
            lower = self.current_hiit_target_bpm - self.error_margin
            upper = self.current_hiit_target_bpm + self.error_margin
            if heart_rate < lower:
                return "below"
            elif heart_rate > upper:
                return "above"
            else:
                return "within"
            
        
    async def safe_exit(self):
        try:
            self.stop_monitoring()
        except:
            pass
        if self.ble_device_manager.is_connected():
            self.ble_device_manager.disconnect()

class Observer:
    def update(self, heart_rate, status):
        # This method should be implemented by the observer classes.
        pass