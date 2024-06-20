import tkinter as tk
from tkinter.font import Font
from datetime import datetime

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.configure(bg='black')
        self.root.geometry("800x600")
        
        self.time_left = 0  # Initial countdown time in seconds
        self.running = False

        # Load the Consolas font for the timer label
        self.custom_font = Font(family="Consolas", size=72)  # Increased size to 72

        # Define button colors
        self.button_colors = {
            'start': {'normal': 'green', 'active': '#295f29', 'disabled': '#808080'},   # Slightly darker green when active, grayed out when disabled
            'stop': {'normal': 'red', 'active': '#6f3c3c', 'disabled': '#808080'},     # Slightly darker red when active, grayed out when disabled
            'reset': {'normal': 'orange', 'active': '#9c6f3c', 'disabled': '#808080'}   # Slightly darker orange when active, grayed out when disabled
        }

        # Timer Label (Entry widget)
        self.timer_label = tk.Entry(self.root, font=self.custom_font, fg='red', bg='#1c1c1c', justify='center', bd=0, insertbackground='red')
        self.timer_label.insert(0, "00:00")
        self.timer_label.pack(fill=tk.X, ipadx=20, ipady=20)  # Adjust ipadx and ipady for size

        # Buttons Frame
        self.buttons_frame = tk.Frame(root, bg='black')
        self.buttons_frame.pack(pady=20)

        self.start_button = tk.Button(self.buttons_frame, text="Start", command=self.start_timer, font=("Helvetica", 14), width=10, height=2,
                                      bg=self.button_colors['start']['normal'], fg='white', activebackground=self.button_colors['start']['active'])
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self.buttons_frame, text="Stop", command=self.stop_timer, font=("Helvetica", 14), width=10, height=2,
                                     bg=self.button_colors['stop']['normal'], fg='white', activebackground=self.button_colors['stop']['active'])
        self.stop_button.config(state=tk.DISABLED, bg=self.button_colors['start']['disabled'])
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_timer, font=("Helvetica", 14), width=10, height=2,
                                      bg=self.button_colors['reset']['normal'], fg='white', activebackground=self.button_colors['reset']['active'])
        self.reset_button.grid(row=0, column=2, padx=10, pady=10)

        # Trace Log Listbox with Scrollbar
        self.trace_log = tk.Listbox(root, bg='#1c1c1c', fg='white', height=10, bd=2, relief='solid', highlightcolor='#fe8500', highlightbackground='#fe8500')
        self.trace_log.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.scrollbar = tk.Scrollbar(self.trace_log, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.trace_log.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.trace_log.yview)

        # Connection Button
        self.connection_button = tk.Button(root, text="Disconnected", command=self.show_connection_menu, anchor='se', bg='black', fg='white')
        self.connection_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.update_timer()
        
    def start_timer(self):
        if not self.running:
            self.running = True
            self.trace_log.insert(tk.END, f"{self.get_current_time()} - Timer started")
            self.trace_log.yview(tk.END)  # Auto-scroll to the end
            self.start_button.config(state=tk.DISABLED, bg=self.button_colors['start']['disabled'])
            self.reset_button.config(state=tk.DISABLED, bg=self.button_colors['reset']['disabled'])
            self.stop_button.config(state=tk.NORMAL, bg=self.button_colors['stop']['normal'])
    
    def stop_timer(self):
        if self.running:
            self.running = False
            self.trace_log.insert(tk.END, f"{self.get_current_time()} - Timer stopped")
            self.trace_log.yview(tk.END)  # Auto-scroll to the end
            self.start_button.config(state=tk.NORMAL, bg=self.button_colors['start']['normal'])
            self.reset_button.config(state=tk.NORMAL, bg=self.button_colors['reset']['normal'])
            self.stop_button.config(state=tk.DISABLED, bg=self.button_colors['stop']['disabled'])
    
    def reset_timer(self):
        self.time_left = 0
        self.timer_label.delete(0, tk.END)
        self.timer_label.insert(0, "00:00")
        self.trace_log.insert(tk.END, f"{self.get_current_time()} - Timer reset")
        self.trace_log.yview(tk.END)  # Auto-scroll to the end
        self.start_button.config(state=tk.NORMAL, bg=self.button_colors['start']['normal'])
        self.stop_button.config(state=tk.DISABLED, bg=self.button_colors['stop']['disabled'])
    
    def update_timer(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_str = f"{minutes:02}:{seconds:02}"
        self.timer_label.delete(0, tk.END)
        self.timer_label.insert(0, time_str)
        
        if self.running:
            self.time_left += 1
        
        self.root.after(1000, self.update_timer)
    
    def show_connection_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Reconnect", command=self.reconnect)
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def reconnect(self):
        self.trace_log.insert(tk.END, f"{self.get_current_time()} - Reconnecting...")
        # Simulate reconnection logic here
        self.connection_button.config(text="Connected")
        self.trace_log.insert(tk.END, f"{self.get_current_time()} - Reconnected")
        self.trace_log.yview(tk.END)  # Auto-scroll to the end
    
    def get_current_time(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()
