import asyncio

class HeartRateMonitor:
    def __init__(self, ble_device_manager, target_zone):
        self.ble_device_manager = ble_device_manager
        self.target_zone = target_zone
        self.observers = []
        self.current_heart_rate = None
        self.status = None

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.current_heart_rate, self.status)

    async def start_monitoring(self):
        if not self.ble_device_manager.is_connected():
            await self.ble_device_manager.connect()
        
        await self.subscribe_to_heart_rate()

    async def stop_monitoring(self):
        await self.unsubscribe_from_heart_rate()

    async def subscribe_to_heart_rate(self):
        HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

        async def notification_handler(sender, data):
            self.process_heart_rate(data)

        await self.ble_device_manager.client.start_notify(HEART_RATE_UUID, notification_handler)

    async def unsubscribe_from_heart_rate(self):
        HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
        await self.ble_device_manager.client.stop_notify(HEART_RATE_UUID)

    def process_heart_rate(self, data):
        flags = data[0]
        is_16bit = flags & 1
        heart_rate = int.from_bytes(data[1:3] if is_16bit else data[1:2], byteorder='little')
        print(f"Heart Rate: {heart_rate} bpm")
        self.current_heart_rate = heart_rate
        self.status = self.in_target_zone(heart_rate)
        self.notify_observers()

    def in_target_zone(self, heart_rate):
        lower, upper = self.target_zone
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