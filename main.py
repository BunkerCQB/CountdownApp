import tkinter as tk
from tkinter.font import Font
from datetime import datetime
from pygame import mixer
import serial
import serial.tools.list_ports
import threading
import os
from tkinter import PhotoImage



mixer.init()

class Config:
    DURATION = 180 #Seconds
    DEAD_BUZZER_TIMER = 5 #Seconds

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Bunker CQB Countdown")
        self.root.configure(bg="black")
        self.root.geometry("800x600")

        icon_path = "icon.ico"
        self.root.iconbitmap(icon_path)

        self.time_left = Config.DURATION
        
        self.running = False
        self.intro_running = False

        self.timer_id = None
        self.intro_id = None
        self.button_active_id = None
        self.first_warning_id = None

        self.buttons_active = False

        self.port = None  # Initialize with None

        self.custom_font = Font(family="Helvetica", size=72, weight="bold")

        # Define button colors
        self.button_colors = {
            "start": {"normal": "green", "active": "#295f29", "disabled": "#808080"},
            "stop": {"normal": "red", "active": "#6f3c3c", "disabled": "#808080"},
            "reset": {"normal": "orange", "active": "#9c6f3c", "disabled": "#808080"},
            "approve": {"normal": "blue", "active": "#295f29", "disabled": "#808080"},
            "test_button": {"normal": "black", "active": "#295f29", "disabled": "#808080"}
        }

        self.entry_frame = tk.Frame(root, bg="#1c1c1c")
        self.entry_frame.pack(fill=tk.X)  # Make the frame span horizontally

        # Configure grid columns to expand
        self.entry_frame.columnconfigure(0, weight=1)  # Expand first column
        self.entry_frame.columnconfigure(1, weight=0)  # Second column (colon label) doesn"t expand
        self.entry_frame.columnconfigure(2, weight=1)  # Expand third column

        # Minutes Entry
        self.minutes_entry = tk.Entry(self.entry_frame, font=self.custom_font, fg="red", bg="#1c1c1c",
                                      justify="right", bd=0, insertbackground="red", width=2, disabledforeground="red", disabledbackground="#1c1c1c")
        self.minutes_entry.grid(row=0, column=0, padx=(10, 2), pady=10, sticky="ew")  # Center horizontally

        vcmd = (self.root.register(self.validate_time_entry), "%P")
        self.minutes_entry.config(validate="key", validatecommand=vcmd)
        self.minutes_entry.bind("<FocusOut>", self.update_time_left)

        # Colon Label
        self.colon_label = tk.Label(self.entry_frame, text=":", font=self.custom_font, fg="red", bg="#1c1c1c", width=1)
        self.colon_label.grid(row=0, column=1, pady=10)

        # Seconds Entry
        self.seconds_entry = tk.Entry(self.entry_frame, font=self.custom_font, fg="red", bg="#1c1c1c",
                                      justify="left", bd=0, insertbackground="red", width=2, disabledforeground="red", disabledbackground="#1c1c1c")
        self.seconds_entry.grid(row=0, column=2, padx=(2, 10), pady=10, sticky="ew")

        self.seconds_entry.config(validate="key", validatecommand=vcmd)
        self.seconds_entry.bind("<FocusOut>", self.update_time_left)

        # Buttons Frame
        self.buttons_frame = tk.Frame(root, bg="black")
        self.buttons_frame.pack(pady=20)

        self.start_button = tk.Button(self.buttons_frame, text="Start", command=self.play_intro, font=("Helvetica", 14),
                                      width=10, height=2, bg=self.button_colors["start"]["normal"], fg="white",
                                      activeforeground="white", activebackground=self.button_colors["start"]["active"])
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self.buttons_frame, text="Stop", command=self.stop_timer, font=("Helvetica", 14),
                                     width=10, height=2, bg=self.button_colors["stop"]["normal"], fg="white",
                                     activeforeground="white", activebackground=self.button_colors["stop"]["active"])
        self.stop_button.config(state=tk.DISABLED, bg=self.button_colors["start"]["disabled"])
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_timer, font=("Helvetica", 14),
                                      width=10, height=2, bg=self.button_colors["reset"]["normal"], fg="white",
                                      activeforeground="white", activebackground=self.button_colors["reset"]["active"])
        self.reset_button.grid(row=0, column=2, padx=10, pady=10)

        self.approve_button = tk.Button(self.buttons_frame, text="Approve", command=self.play_approval, font=("Helvetica", 14),
                                      width=10, height=2, bg=self.button_colors["approve"]["normal"], fg="white",
                                      activeforeground="white", activebackground=self.button_colors["reset"]["active"])
        self.approve_button.grid(row=0, column=3, padx=10, pady=10)
        
        self.test_button = tk.Button(self.buttons_frame, text="Dead Button Test", command=self.play_first_warning, font=("Helvetica", 14),
                                      width=15, height=1, bg=self.button_colors["test_button"]["normal"], fg="white",
                                      activeforeground="white", activebackground=self.button_colors["test_button"]["active"])
        self.test_button.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        # Trace Log Listbox with Scrollbar
        self.trace_log = tk.Listbox(root, bg="#1c1c1c", fg="white", height=10, bd=2, relief="solid",
                                    highlightcolor="#fe8500", highlightbackground="#fe8500", font=("Helvetica", 14))
        self.trace_log.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.scrollbar = tk.Scrollbar(self.trace_log, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.trace_log.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.trace_log.yview)
        
        self.port = self.find_arduino_port()
        
        self.update_timer()

    def play_intro(self):
        self.intro_running = True
        self.update_time_left(None)
        mixer.music.load("./sounds/30SecondsStart.mp3")
        mixer.music.play()
        self.insert_log("Playing intro...", "green")

        # Disabled start, edit and enabled stop
        self.start_button.config(state=tk.DISABLED, bg=self.button_colors["start"]["disabled"])
        self.reset_button.config(state=tk.DISABLED, bg=self.button_colors["reset"]["disabled"])
        self.stop_button.config(state=tk.NORMAL, bg=self.button_colors["stop"]["normal"])

        # Disabled edit the timer
        self.minutes_entry.config(state="disabled")
        self.seconds_entry.config(state="disabled")

        self.intro_id = self.root.after(30000, self.start_timer)

    def play_approval(self):
        mixer.music.load("./sounds/PointApproved.mp3")
        mixer.music.play()
        self.insert_log("Point Approved", "orange")
        
    def start_timer(self):
        self.intro_running = False

        if not self.running:
            self.running = True
            self.intro_id = None

            self.insert_log("Timer started")
            self.button_active_id = self.root.after(30 * 1000, self.activate_button)
            
            self.update_timer()

    def stop_timer(self):
        self.intro_running = False
        self.running = False

        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if self.button_active_id:
            self.root.after_cancel(self.button_active_id)
            self.button_active_id = None

        self.buttons_active = False

        self.start_button.config(state=tk.NORMAL, bg=self.button_colors["start"]["normal"])
        self.reset_button.config(state=tk.NORMAL, bg=self.button_colors["reset"]["normal"])
        self.stop_button.config(state=tk.DISABLED, bg=self.button_colors["stop"]["disabled"])

        # Enabled edit the timer
        self.minutes_entry.config(state="normal")
        self.seconds_entry.config(state="normal")
    
        
        if self.running:
            self.insert_log("Timer stopped")
        else:
            if self.intro_id:
                self.insert_log("Cancelling intro", "red")
                self.root.after_cancel(self.intro_id)
                self.intro_id = None

            if not self.first_warning_id:
                self.insert_log("Round Over!", "orange")

            mixer.music.load("./sounds/3BeepEnd.mp3")
            mixer.music.play()

    def validate_time_entry(self, new_value):
        if new_value.isdigit() or new_value == "":
            return len(new_value) <= 2  # Limit input to 2 characters (for minutes and seconds)
        else:
            return False

    def update_time_left(self, event):
        minutes_text = self.minutes_entry.get()
        seconds_text = self.seconds_entry.get()

        try:
            minutes = int(minutes_text) if minutes_text else 0
            seconds = int(seconds_text) if seconds_text else 0
            self.time_left = minutes * 60 + seconds
            self.update_timer_label()
        except ValueError:
            pass 

    def reset_timer(self):
        self.time_left = Config.DURATION
        self.update_timer_label()
        self.insert_log("Timer reset")

    def update_timer(self):
        self.update_timer_label()

        if self.running:
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                self.running = False

                # Play the sound file
                mixer.music.load("./sounds/3BeepEnd.mp3")
                mixer.music.play()
                self.insert_log("Playing outro...", "orange")

                self.insert_log("Timer finished")
                self.start_button.config(state=tk.NORMAL, bg=self.button_colors["start"]["normal"])
                self.reset_button.config(state=tk.NORMAL, bg=self.button_colors["reset"]["normal"])
                self.stop_button.config(state=tk.DISABLED, bg=self.button_colors["stop"]["disabled"])
                self.time_left = Config.DURATION

                if self.button_active_id:
                    self.root.after_cancel(self.button_active_id)

                if self.first_warning_id:
                    self.root.after_cancel(self.first_warning_id)

                self.timer_id = None
                self.intro_id = None
                self.button_active_id = None
                self.first_warning_id = None

                self.minutes_entry.config(state="normal")
                self.seconds_entry.config(state="normal")


    def get_current_time(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")
    
    def convert_time_to_total_seconds(self, time_str):
        if len(time_str) != 4:
            raise ValueError("Invalid time format. Expected format is \"HHMM\".")

        hours = int(time_str[:2])
        minutes = int(time_str[2:])

        total_seconds = hours * 60 + minutes

        return total_seconds

    def update_timer_label(self):
        # using time left to update the timer label
        minutes = self.time_left // 60
        seconds = self.time_left % 60

        if self.running:
            self.minutes_entry.config(state="normal")
            self.seconds_entry.config(state="normal")

        self.minutes_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, f"{minutes:02}")

        self.seconds_entry.delete(0, tk.END)
        self.seconds_entry.insert(0, f"{seconds:02}")

        if self.running:
            self.minutes_entry.config(state="disabled")
            self.seconds_entry.config(state="disabled")

    def insert_log(self, text, color = "white"):
        self.trace_log.insert(tk.END, f"{self.get_current_time()} - {text}")
        self.trace_log.itemconfig(tk.END, {"fg": color})
        self.trace_log.yview(tk.END)  
    def insert_log(self, text, color = "white"):
        self.trace_log.insert(tk.END, f"{self.get_current_time()} - {text}")
        self.trace_log.itemconfig(tk.END, {"fg": color})
        self.trace_log.yview(tk.END)  
    
    def activate_button(self):
        self.insert_log("Dead Buttons are now activated!", "orange")
        self.button_active_id = None
        self.buttons_active = True

    def find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        self.insert_log("Trying to find COM port!")
        if ports:
            for p in ports:
             if "Arduino" in p.description:
                port = p  # Select the first available COM port
                self.insert_log(f"COM port found: {port.device}", "green")
                self.connect_to_arduino(port.device)
                return port.device
    
        self.insert_log("COM port not found!", "red")
        self.insert_log("Please try fix & reopen the program", "red")
        return None
    
    def connect_to_arduino(self, port):
        try:
            self.serial_connection = serial.Serial(port, 9600)
            self.insert_log(f"Connected to {port}", "green")
            threading.Thread(target=self.read_from_serial, daemon=True).start()
        except Exception as e:
            self.insert_log(f"Failed to connect: {e}", "red")

    def read_from_serial(self):
        self.insert_log("Listening for data from serial", "green")
        while self.serial_connection and self.serial_connection.is_open:
            try:
                data = self.serial_connection.readline().strip().decode("utf-8")
                if data == "Left" or data == "Right":
                    if self.buttons_active:
                        if not self.first_warning_id:
                            self.insert_log(f"{data.upper()} button has been clicked!", "purple")
                            self.play_first_warning()
                        else:
                            self.insert_log(f"{data.upper()} tried click button but it already has been clicked!", "red")

                    else:
                        self.insert_log(f"{data.upper()} button has been clicked but buttons are not yet active!", "purple")
                
            except Exception as e:
                self.insert_log(f"Error: {e}", "red")
                break

    def play_first_warning(self):
        self.insert_log("Playing first warning", "orange")
        self.insert_log("Round will end in " + str(Config.DEAD_BUZZER_TIMER) + " seconds!", "orange")

        mixer.music.load("./sounds/DeadBuzzerEdit.mp3")
        mixer.music.play()

        self.first_warning_id = self.root.after(Config.DEAD_BUZZER_TIMER*1000, self.stop_timer)


if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()
