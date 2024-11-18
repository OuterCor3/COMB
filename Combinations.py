from itertools import combinations

# Example dataset
data = [
    ['A', 'B', 'C', 'D', 'E'],  # Row 1
    ['F', 'G', 'H', 'I', 'J']   # Row 2
]

def row_combinations(data, r=None):
    all_combinations = []
    for row in data:
        r = r if r else len(row)  # Default to full row length
        all_combinations.append(list(combinations(row, r)))
    return all_combinations

result = row_combinations(data, r=3)  # Combinations of size 3 for each row
print("Row-wise combinations:")
for row_result in result:
    print(row_result)
