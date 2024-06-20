import tkinter as tk
from tkinter.font import Font
from datetime import datetime


class Config:
    DURATION = 5


class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.configure(bg='black')
        self.root.geometry("800x600")

        self.time_left = Config.DURATION
        self.running = False
        self.timer_id = None

        self.override = False

        # Load the Consolas font for the timer label
        self.custom_font = Font(family="Consolas", size=72)

        # Define button colors
        self.button_colors = {
            'start': {'normal': 'green', 'active': '#295f29', 'disabled': '#808080'},
            'stop': {'normal': 'red', 'active': '#6f3c3c', 'disabled': '#808080'},
            'reset': {'normal': 'orange', 'active': '#9c6f3c', 'disabled': '#808080'}
        }

        # Timer Label (Entry widget)
        vcmd = (self.root.register(self.validate_time_entry), '%P')
        self.timer_label = tk.Entry(self.root, font=self.custom_font, fg='red', bg='#1c1c1c',
                                    readonlybackground='#1c1c1c', justify='center', bd=0, insertbackground='red',
                                    validate='key', validatecommand=vcmd)
                                    
        self.timer_label.pack(fill=tk.X, ipadx=20, ipady=20)

        # Buttons Frame
        self.buttons_frame = tk.Frame(root, bg='black')
        self.buttons_frame.pack(pady=20)

        self.start_button = tk.Button(self.buttons_frame, text="Start", command=self.start_timer, font=("Helvetica", 14),
                                      width=10, height=2, bg=self.button_colors['start']['normal'], fg='white',
                                      activeforeground="white", activebackground=self.button_colors['start']['active'])
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self.buttons_frame, text="Stop", command=self.stop_timer, font=("Helvetica", 14),
                                     width=10, height=2, bg=self.button_colors['stop']['normal'], fg='white',
                                     activeforeground="white", activebackground=self.button_colors['stop']['active'])
        self.stop_button.config(state=tk.DISABLED, bg=self.button_colors['start']['disabled'])
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_timer, font=("Helvetica", 14),
                                      width=10, height=2, bg=self.button_colors['reset']['normal'], fg='white',
                                      activeforeground="white", activebackground=self.button_colors['reset']['active'])
        self.reset_button.grid(row=0, column=2, padx=10, pady=10)

        # Trace Log Listbox with Scrollbar
        self.trace_log = tk.Listbox(root, bg='#1c1c1c', fg='white', height=10, bd=2, relief='solid',
                                    highlightcolor='#fe8500', highlightbackground='#fe8500')
        self.trace_log.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.scrollbar = tk.Scrollbar(self.trace_log, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.trace_log.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.trace_log.yview)

        # Connection Button
        self.connection_button = tk.Button(root, text="Disconnected", command=self.show_connection_menu, anchor='se',
                                           bg='black', fg='white')
        self.connection_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.update_timer()

    def validate_time_entry(self, new_value):
        print(self.running)
        print(self.override)
        if self.running or self.override:
            print("Ovveride")
            return True
        
        # if len(new_value) == 5 and new_value[2] == ":" and new_value.replace(":", "").isdigit():
        #     print("pass logic")
        #     return True

        # digits = new_value.replace(":", "")

        # if "0" not in digits:
        #     print("no zeros")
        #     return False

        # new_digits = digits[-4:]
        # self.time_left = self.convert_time_to_total_seconds(new_digits)
        # self.timer_label.delete(0, tk.END)
        # self.timer_label.insert(0, self.get_formatted_countdown_time())


        # Ensure the new value contains only digits and is at most 4 characters long
    
    def start_timer(self):
        if not self.running:
            self.running = True
            self.trace_log.insert(tk.END, f"{self.get_current_time()} - Timer started")
            self.trace_log.yview(tk.END)
            self.start_button.config(state=tk.DISABLED, bg=self.button_colors['start']['disabled'])
            self.reset_button.config(state=tk.DISABLED, bg=self.button_colors['reset']['disabled'])
            self.stop_button.config(state=tk.NORMAL, bg=self.button_colors['stop']['normal'])
            self.update_timer()

    def stop_timer(self):
        if self.running:
            self.running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            self.trace_log.insert(tk.END, f"{self.get_current_time()} - Timer stopped")
            self.trace_log.yview(tk.END)
            self.start_button.config(state=tk.NORMAL, bg=self.button_colors['start']['normal'])
            self.reset_button.config(state=tk.NORMAL, bg=self.button_colors['reset']['normal'])
            self.stop_button.config(state=tk.DISABLED, bg=self.button_colors['stop']['disabled'])
            self.timer_label.config(state='normal')

    def reset_timer(self):
        self.time_left = Config.DURATION
        self.timer_label.config(state='normal')
        self.change_timer_label(self.get_formatted_countdown_time())
        self.timer_label.config(state='readonly')
        self.trace_log.insert(tk.END, f"{self.get_current_time()} - Timer reset")
        self.trace_log.yview(tk.END)
        self.start_button.config(state=tk.NORMAL, bg=self.button_colors['start']['normal'])
        self.stop_button.config(state=tk.DISABLED, bg=self.button_colors['stop']['disabled'])

    def update_timer(self):
        print(self.get_formatted_countdown_time())
        self.change_timer_label(self.get_formatted_countdown_time())
w
        if self.running:
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                self.running = False
                self.trace_log.insert(tk.END, f"{self.get_current_time()} - Timer finished")
                self.trace_log.yview(tk.END)
                self.start_button.config(state=tk.NORMAL, bg=self.button_colors['start']['normal'])
                self.reset_button.config(state=tk.NORMAL, bg=self.button_colors['reset']['normal'])
                self.stop_button.config(state=tk.DISABLED, bg=self.button_colors['stop']['disabled'])
                self.time_left = Config.DURATION
                self.timer_id = None

    def get_formatted_countdown_time(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes:02}:{seconds:02}"

    def show_connection_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Reconnect", command=self.reconnect)
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def reconnect(self):
        self.trace_log.insert(tk.END, f"{self.get_current_time()} - Reconnecting...")
        self.connection_button.config(text="Connected")
        self.trace_log.insert(tk.END, f"{self.get_current_time()} - Reconnected")
        self.trace_log.yview(tk.END)

    def get_current_time(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")
    
    def convert_time_to_total_seconds(self, time_str):
        if len(time_str) != 4:
            raise ValueError("Invalid time format. Expected format is 'HHMM'.")

        hours = int(time_str[:2])
        minutes = int(time_str[2:])

        total_seconds = hours * 60 + minutes

        return total_seconds
    
    def change_timer_label(self, text):
        self.override = True
        self.timer_label.delete(0, tk.END)
        self.timer_label.insert(0, text)
        self.override = False


if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()
