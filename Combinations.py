from itertools import chain, combinations

# Function to generate power set of a list
def power_set(data):
    return list(chain.from_iterable(combinations(data, r) for r in range(len(data) + 1)))

# Function to generate row-wise combinations
def row_combinations(data, r=None):
    all_combinations = []
    for row in data:
        r = r if r else len(row)  # Default to full row length
        all_combinations.append(list(combinations(row, r)))
    return all_combinations

# Get user input
columns = input("Enter column names separated by commas (e.g., Col1,Col2,Col3,Col4,Col5): ").split(',')
rows = int(input("Enter the number of rows in your dataset: "))

# Input data row-by-row
data = []
print("Enter the data row-by-row:")
for i in range(rows):
    row = input(f"Row {i + 1} (values separated by commas): ").split(',')
    data.append(row)

# Perform operations
print("\n1. Generate power set of columns")
print("2. Generate row-wise combinations of a specific size")
choice = int(input("Enter your choice (1 or 2): "))

if choice == 1:
    subsets = power_set(columns)
    print("\nAll possible column subsets:")
    for subset in subsets:
        print(subset)
elif choice == 2:
    r = int(input("Enter the combination size (e.g., 2 for pairs): "))
    row_combos = row_combinations(data, r)
    print(f"\nRow-wise combinations of size {r}:")
    for i, combos in enumerate(row_combos, start=1):
        print(f"Row {i}: {combos}")
else:
    print("Invalid choice!")
