import asyncio
import websockets
import tkinter as tk
from tkinter import ttk
from threading import Thread

# A dictionary to store connected clients and their addresses
connected_clients = {}
checkbox_vars = {}  # Dictionary to store reference to checkbutton variables

async def send_message_to_clients(message, clients):
    """Send a message to selected WebSocket clients."""
    if clients:
        await asyncio.gather(*(client.send(message) for client in clients))

async def handle_client(websocket, path):
    """Handles an incoming WebSocket connection."""
    # Register the client
    address = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    connected_clients[address] = websocket
    checkbox_vars[address] = tk.BooleanVar()  # Add a BooleanVar for the new client

    # Update checkboxes in the GUI
    update_checkboxes()

    print(f"Client connected: {address}")
    
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            await send_message_to_clients(f"Server received: {message}", connected_clients.values())
    except websockets.ConnectionClosed:
        print(f"Connection with client closed: {address}")
    finally:
        # Unregister the client
        del connected_clients[address]
        del checkbox_vars[address]  # Remove the BooleanVar for the disconnected client
        update_checkboxes()  # Update checkboxes when client disconnects

async def websocket_server():
    """Start the WebSocket server."""
    async with websockets.serve(handle_client, "localhost", 3000):
        await asyncio.Future()  # run forever

def start_server():
    """Run the WebSocket server in a separate thread."""
    asyncio.run(websocket_server())

def on_send_button_click():
    """Callback function for the 'Send' button click."""
    message = input_entry.get()
    if message:
        # Get selected clients
        selected_clients = [websocket for address, websocket in connected_clients.items() if checkbox_vars.get(address, tk.BooleanVar()).get()]
        if selected_clients:
            asyncio.run(send_message_to_clients(f"Server says: {message}", selected_clients))
        input_entry.delete(0, tk.END)

def update_checkboxes():
    """Update the checkboxes with the current connected clients."""
    global checkboxes_frame, canvas, scrollbar

    # Clear old checkboxes
    for widget in checkboxes_frame.winfo_children():
        widget.destroy()
    
    if not connected_clients:
        tk.Label(checkboxes_frame, text="No clients connected").pack(anchor='w')
    else:
        for address in connected_clients.keys():
            tk.Checkbutton(checkboxes_frame, text=address, variable=checkbox_vars[address]).pack(anchor='w')

    # Update scroll region of the canvas
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Tkinter GUI setup
def create_gui():
    global input_entry, checkboxes_frame, root, canvas, scrollbar

    root = tk.Tk()
    root.title("WebSocket Server")

    # Create a frame for the checkboxes
    checkbox_frame = tk.Frame(root)
    checkbox_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Create a canvas widget for the checkboxes
    canvas = tk.Canvas(checkbox_frame, borderwidth=0)
    scrollbar = tk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
    checkboxes_frame = tk.Frame(canvas)

    # Place the checkboxes frame inside the canvas
    checkboxes_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=checkboxes_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Configure row and column weights to expand the canvas and scrollbar
    checkbox_frame.grid_rowconfigure(0, weight=1)
    checkbox_frame.grid_columnconfigure(0, weight=1)
    checkbox_frame.grid_columnconfigure(1, weight=0)

    # Create a label and entry field for the message
    label = tk.Label(root, text="Enter message:")
    label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    input_entry = tk.Entry(root, width=50)
    input_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    # Create a send button
    send_button = tk.Button(root, text="Send", command=on_send_button_click)
    send_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    # Configure row and column weights
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=0)
    root.grid_columnconfigure(0, weight=1)

    root.geometry("400x300")
    root.mainloop()

if __name__ == "__main__":
    # Start WebSocket server in a separate thread
    server_thread = Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Start Tkinter GUI
    create_gui()
