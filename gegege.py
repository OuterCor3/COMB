import tkinter as tk
from tkinter import simpledialog, scrolledtext, filedialog, messagebox
import csv
from itertools import product, combinations_with_replacement


class ColumnCombinations:
    def __init__(self, master):
        self.master = master
        self.master.title("Column Combinations Generator")
        self.columns = []
        self.row_contents = []
        self.max_values = []
        self.combinations = []

        self.setup_ui()

    def setup_ui(self):
        self.master.grid_columnconfigure(0, weight=1, minsize=300)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=2)

        num_columns = simpledialog.askinteger("Columns", "How many columns do you want?", minvalue=1, maxvalue=10)
        if num_columns is None:
            self.master.quit()
            return

        for i in range(num_columns):
            column_name = simpledialog.askstring("Column Name", f"Enter name for column {i + 1}")
            if column_name is None:
                self.master.quit()
                return
            self.columns.append(column_name)

            row_data = simpledialog.askstring("Row Content", f"Enter comma-separated values for '{column_name}'")
            if row_data is None:
                self.master.quit()
                return
            rows = [item.strip() for item in row_data.split(',')]
            self.row_contents.append(rows)

            max_val = simpledialog.askinteger("Max Value", f"Enter the maximum total for '{column_name}'")
            if max_val is None:
                self.master.quit()
                return
            self.max_values.append(max_val)

        self.result_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=50, height=20)
        self.result_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        generate_button = tk.Button(self.master, text="Generate Combinations", command=self.generate_combinations)
        generate_button.grid(row=2, column=0, pady=5, sticky="ew")

        save_button = tk.Button(self.master, text="Save as CSV", command=self.save_to_csv)
        save_button.grid(row=3, column=0, pady=5, sticky="ew")

    def generate_combinations(self):
        column_combinations = []
        for i, rows in enumerate(self.row_contents):
            max_val = self.max_values[i]
            column_combinations.append(self.generate_column_combinations(rows, max_val))

        self.combinations = list(product(*column_combinations))
        self.display_combinations()

    def generate_column_combinations(self, rows, max_val):
        combinations = []
        for combo in combinations_with_replacement(range(len(rows)), max_val):
            counts = [combo.count(i) for i in range(len(rows))]
            formatted = [f"{count} pcs {rows[i]}" for i, count in enumerate(counts) if count > 0]
            if sum(counts) == max_val:
                combinations.append(" | ".join(formatted))
        return combinations

    def display_combinations(self):
        self.result_text.delete('1.0', tk.END)
        if not self.combinations:
            self.result_text.insert(tk.END, "No combinations generated.\n")
            return

        for combo in self.combinations:
            self.result_text.insert(tk.END, f"{combo}\n")

    def save_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Combinations"])
                    for combo in self.combinations:
                        writer.writerow([combo])
                messagebox.showinfo("Success", f"Combinations saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ColumnCombinations(root)
    root.mainloop()
