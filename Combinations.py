import tkinter as tk
from tkinter import simpledialog, scrolledtext
from itertools import product

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

        self.result_text = scrolledtext.ScrolledText(self.master, width=50, height=20)
        self.result_text.grid(row=2, column=0, columnspan=len(self.columns), padx=10, pady=10, sticky="nsew")

    def generate_combinations(self):
        self.combinations = list(product(*self.row_contents))  # Generate cartesian product of rows

        self.display_combinations()

    def display_combinations(self):
        self.result_text.delete('1.0', tk.END)
        for combo in self.combinations:
            self.result_text.insert(tk.END, f"{' + '.join(combo)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColumnCombinations(root)
    root.mainloop()
