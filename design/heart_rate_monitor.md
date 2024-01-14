# HeartRateMonitor

#### Responsibilities and Functionalities:

1. **Monitor Real-Time Heart Rate Data**:
   - Continuously receive and update the heart rate data from the BLE device.
   - This involves interacting with the `BLEDeviceManager` to ensure a constant flow of data.

2. **Process and Interpret Heart Rate Data**:
   - Analyze the incoming heart rate data to determine its status relative to the target heart rate zone (below, within, or above the target zone).

3. **Manage Observers (Observer Pattern Implementation)**:
   - Maintain a list of observer objects that are interested in heart rate data updates.
   - This includes registering new observers and notifying them of any changes.

4. **Notify Observers of State Changes**:
   - Whenever there's a change in the heart rate data or its status, notify all registered observers.
   - Each observer should then react accordingly based on its own logic (e.g., `FeedbackSystem` may provide user feedback, `DataLogger` may log the data).

6. [**Tentative**] **Handle Start and Stop of Monitoring**:
   - Provide methods to start and stop the heart rate monitoring, which might involve initializing or closing the connection with the BLE device.


#### Preliminary Design:

##### Attributes:
- `ble_device_manager`: Instance of `BLEDeviceManager` to use for connecting to the BLE device.
- `target_bpm`: The currently targeted heart rate zone .
- `error_margin`: The threshold of tolerence for `target_bpm` (e.g. +/- 5 bpm)
- `observers`: A list to keep track of registered observer objects.
- `current_heart_rate`: Stores the latest heart rate reading.
- `status`: Indicates the current status of the heart rate relative to the target zone.

##### Methods:
- `__init__(self, ble_device_manager, target_bpm, error_margin)`: Constructor to initialize with a BLE device manager and target zone.
- `start_monitoring(self)`: Start receiving and processing heart rate data.
- `stop_monitoring(self)`: Stop the heart rate data monitoring.
- `process_heart_rate(self, data)`: Process the received heart rate data.
- `in_target_zone(self, heart_rate)`: Determine if the given heart rate is within the target zone.
- `register_observer(observer)`: Adds a new observer to the list.
- `notify_observers()`: Notifies all registered observers about a change in heart rate or status.

#### Implementation Considerations:
- **Asynchronous Data Handling**: The module should handle heart rate data asynchronously.
- **Real-Time Processing**: It should process heart rate data in real-time as it is received.
- **Integration with BLEDeviceManager**: This module depends on `BLEDeviceManager` for receiving heart rate data.
- **Error Handling**: Robust error handling for scenarios such as data reception issues or processing errors.
