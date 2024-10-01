import sys
import csv

input_file = sys.argv[1]
output_file = sys.argv[2]
changes = sys.argv[3:]

# Wczytaj plik wejściowy
with open(input_file, mode='r', newline='') as infile:
    reader = csv.reader(infile)
    data = list(reader)

# Wprowadź zmiany
for change in changes:
    row, col, new_value = change.split(",")
    row, col = int(row), int(col)
    data[row][col] = new_value

# Zapisz plik wyjściowy
with open(output_file, mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data)

print(f"Input file: {input_file}")
print(f"Output file: {output_file}")
print("Changes applied:")
for change in changes:
    row, col, new_value = change.split(",")
    print(f"row: {row}, column {col}, new value {new_value}")

