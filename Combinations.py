import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from itertools import combinations

class ColumnCombinations:
    def __init__(self, master):
        self.master = master
        self.master.title("Column Combinations Generator")
        self.columns = []
        self.combinations = []

        self.setup_ui()

    def setup_ui(self):
        num_columns = simpledialog.askinteger("Columns", "How many columns do you want?", minvalue=1, maxvalue=10)
        
        for i in range(num_columns):
            column_name = simpledialog.askstring("Column Name", f"Enter name for column {i+1}")
            self.columns.append(column_name)

        for i, column in enumerate(self.columns):
            tk.Label(self.master, text=column, font=('Arial', 12, 'bold')).grid(row=0, column=i, padx=5, pady=5)

        tk.Button(self.master, text="Generate Combinations", command=self.generate_combinations).grid(row=1, column=0, columnspan=len(self.columns), pady=10)

        self.result_text = scrolledtext.ScrolledText(self.master, width=50, height=20)
        self.result_text.grid(row=2, column=0, columnspan=len(self.columns), padx=10, pady=10)

    def generate_combinations(self):
        self.combinations = []
        for r in range(1, len(self.columns) + 1):
            self.combinations.extend(combinations(self.columns, r))
        
        self.display_combinations()

    def display_combinations(self):
        self.result_text.delete('1.0', tk.END) 
        for combo in self.combinations:
            self.result_text.insert(tk.END, f"{' + '.join(combo)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColumnCombinations(root)
    root.mainloop()
