# GUI

### Responsibilities and Functionalities:

The `GUI` serves as the primary interface for the user to interact with the application and receive real-time feedback on their heart rate. For the sake of simplicity it consolidates the responsabilities you'd expect to see in both the GUI and Controller modules into a single module for now.

1. **Visual Feedback**:
   - Use color codes or other visual elements to indicate the current heart rate zone status.

2. **Heart Rate Display**:
   - Prominently show the current heart rate.

3. **Control Heart Rate Monitoring**:
   - Issue commands to start or stop monitoring.

4. **Error Messaging**:
   - Display error messages or alerts as needed (e.g. if connection is lost).

5. **Close Application**:
   - Provide a mechanism for the user to safely exit the application.

### Preliminary Design:

#### Attributes:
- `heart_rate_label`: UI element to display the heart rate.
- `start_stop_button`: Button to toggle the monitoring state.
- `background`: Background element whose color reflects the heart rate zone.

#### Methods:
- `initialize_ui(self)`: Sets up the UI elements and initial state.
- `update_heart_rate_display(self, heart_rate)`: Updates the heart rate display.
- `update_background_color(self, zone_status)`: Changes the background color based on the heart rate zone.
- `start_stop_monitoring(self)`: Starts or stops the heart rate monitoring.
- `show_error_message(self, message)`: Displays an error message.
- `on_exit(self)`: Handles the application exit process.

### Implementation Considerations:

- **Tkinter and Asyncio Integration**: Careful integration of Tkinter's event loop with Python's `asyncio` to manage asynchronous operations without freezing the GUI.

- **Responsive Design**: Ensure that the GUI remains responsive, updating in real-time without significant delays.

- **Error Handling**: Implement comprehensive error handling within the GUI to manage scenarios like disconnection or unavailable data.

- **Modular Design**: Structure the code in a way that allows for easy extension or modification of the GUI components.
