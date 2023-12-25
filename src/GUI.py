import asyncio
import tkinter as tk
from tkinter import ttk

# Example tkinter application
class GUI(tk.Tk):
    def __init__(self, loop, heart_rate_monitor):
        super().__init__()
        self.loop = loop
        self.heart_rate_monitor = heart_rate_monitor
        self.WARNING_COLOR = '#FBCBCB'
        self.NEUTRAL_COLOR = '#F0F0F0'
        self.POSITIVE_COLOR = '#CBFBD5'
        self.primary_color = '#282828'
        self.background_color = self.NEUTRAL_COLOR

        # Set the window size and remove the title bar
        self.geometry("800x600")
        #self.overrideredirect(True)  # This removes the title bar

        # Set the background color
        self.configure(bg=self.background_color)  # Example pink background

        # Heart Rate Label
        self.heart_rate_label = tk.Label(self, text="---", font=("Helvetica", 48),bg=self.background_color, fg=self.primary_color)
        self.heart_rate_label.place(relx=0.5, rely=0.4, anchor='center')

        # Start/Stop Button
        # Create a custom style for the buttons with rounded corners
        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Helvetica', 16), borderwidth=0)
        # Modify the following line to set the background and foreground color correctly
        self.style.configure('TButton', background=self.primary_color, foreground=self.background_color)

        # Start button
        self.start_button = ttk.Button(self, text="Start", style='TButton', command=self.start_monitoring)
        self.start_button.place(relx=0.5, rely=0.6, anchor='center', width=150, height=50)

        # Stop button
        self.stop_button = ttk.Button(self, text="Stop", style='TButton', command=self.stop_monitoring)
        self.stop_button.place(relx=0.5, rely=0.7, anchor='center', width=150, height=50)

        # Exit protocol
        self.protocol("WM_DELETE_WINDOW", self.on_exit)


    def start_monitoring(self):
        # Schedule start_monitoring in the asyncio event loop
        asyncio.run_coroutine_threadsafe(self.heart_rate_monitor.start_monitoring(), self.loop)

    def stop_monitoring(self):
        # Schedule stop_monitoring in the asyncio event loop
        asyncio.run_coroutine_threadsafe(self.heart_rate_monitor.stop_monitoring(), self.loop)

    def on_exit(self):
        asyncio.run_coroutine_threadsafe(self.heart_rate_monitor.stop_monitoring(), self.loop)
        asyncio.run_coroutine_threadsafe(self.heart_rate_monitor.safe_exit(), self.loop)
        self.destroy()

    def update(self, heart_rate, status):
        self.heart_rate_label["text"] = f"{heart_rate}"
        if status == "within":
            self.background_color = self.POSITIVE_COLOR
        elif status == "below" or status == "above":
            self.background_color = self.WARNING_COLOR

        self.configure(bg=self.background_color)  # Example pink background
        self.heart_rate_label.configure(bg=self.background_color)
        self.style.configure('TButton', background=self.primary_color, foreground=self.background_color)