import asyncio
from bleak import BleakClient

class BLEDeviceManager:
    def __init__(self, address):
        self.address = address
        self.client = None

    async def connect(self, max_retries=5, initial_delay=1):
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                self.client = BleakClient(self.address)
                await self.client.connect()
                if self.client.is_connected:
                    print(f"Connected to {self.address}")
                    return True
                else:
                    print(f"Retrying connection to {self.address} in {delay} seconds...")
                    await asyncio.sleep(delay)
                    delay *= 2  # Exponential backoff
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(delay)
                delay *= 2

        print(f"Failed to connect to {self.address} after {max_retries} attempts.")
        return False

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            print(f"Disconnected from {self.address}")

    def is_connected(self):
        return self.client.is_connected if self.client else False
        