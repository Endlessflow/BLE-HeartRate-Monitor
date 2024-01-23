import asyncio
import tkinter as tk
from tkinter import ttk

# Example tkinter application
class GUI(tk.Tk):
    def __init__(self, loop, heart_rate_monitor):
        super().__init__()
        self.loop = loop
        self.heart_rate_monitor = heart_rate_monitor
        
        # Define a color scheme
        self.colors = {
            'warning': '#FBCBCB',
            'neutral': '#F0F0F0',
            'positive': '#CBFBD5',
            'primary': '#282828',
        }

        # Set the window size
        self.geometry("800x600")

        # Set the background color
        self.configure(bg=self.colors['neutral'])

        # Use frames to organize the layout
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side="top", fill="both", expand=True)
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(side="bottom", fill="x")

        # Heart Rate Label
        self.heart_rate_label = tk.Label(self.top_frame, text="---", font=("Helvetica", 48), bg=self.colors['neutral'], fg=self.colors['primary'])
        self.heart_rate_label.pack(side="top", fill="both", expand=True, pady=20)

        # Create and style buttons
        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Helvetica', 16), borderwidth=0)

        # Define a method to update button styling
        self.update_button_style('neutral')

        # Define buttons and place them within the bottom frame
        self.start_button = ttk.Button(self.bottom_frame, text="Start", command=self.start_monitoring)
        self.start_button.pack(side="left", padx=10, pady=10)

        self.stop_button = ttk.Button(self.bottom_frame, text="Stop", command=self.stop_monitoring)
        self.stop_button.pack(side="left", padx=10, pady=10)

        self.hiit_start_button = ttk.Button(self.bottom_frame, text="Start HIIT", command=self.start_hiit)
        self.hiit_start_button.pack(side="left", padx=10, pady=10)

        self.hiit_stop_button = ttk.Button(self.bottom_frame, text="Stop HIIT", command=self.stop_hiit)
        self.hiit_stop_button.pack(side="left", padx=10, pady=10)

        # Exit protocol
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Additional labels for HIIT information
        self.hiit_phase_label = tk.Label(self.top_frame, text="Phase: ---", font=("Helvetica", 16))
        self.hiit_phase_label.pack()
        self.hiit_cycle_count_label = tk.Label(self.top_frame, text="Cycle: ---", font=("Helvetica", 16))
        self.hiit_cycle_count_label.pack()
        self.hiit_target_bpm_label = tk.Label(self.top_frame, text="Target BPM: ---", font=("Helvetica", 16))
        self.hiit_target_bpm_label.pack()

    def update_button_style(self, status):
        color = self.colors.get(status, self.colors['neutral'])
        self.style.configure('TButton', background=color, foreground=self.colors['primary'])

    def start_hiit(self):
        asyncio.run_coroutine_threadsafe(self.heart_rate_monitor.start_hiit_workout(), self.loop)

    def stop_hiit(self):
        asyncio.run_coroutine_threadsafe(self.heart_rate_monitor.stop_hiit_workout(), self.loop)
 
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

    def update(self, heart_rate, status, hiit_active=False, hiit_phase=None, hiit_cycle_count=None, hiit_target_bpm=None):
        self.heart_rate_label["text"] = f"{heart_rate}"
        if status == "within":
            self.background_color = self.colors["positive"]
        elif status == "below" or status == "above":
            self.background_color = self.colors["warning"]

        self.configure(bg=self.background_color)  # Example pink background
        self.heart_rate_label.configure(bg=self.background_color)

        # Update the GUI based on HIIT status
        if hiit_active:
            if hiit_phase is not None and hiit_target_bpm is not None:
                self.hiit_phase_label["text"] = f"Phase: {hiit_phase}"
                self.hiit_cycle_count_label["text"] = f"Cycle: {hiit_cycle_count}"
                self.hiit_target_bpm_label["text"] = f"Target BPM: {hiit_target_bpm}"
        else:
            # Hide or reset the HIIT labels if not in HIIT mode
            self.hiit_phase_label["text"] = "Phase: ---"
            self.hiit_target_bpm_label["text"] = "Target BPM: ---"

        self.update_button_style(status)