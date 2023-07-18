import json
import csv
from deepdiff import DeepDiff

def flatten_dict(d, prefix=''):
    flat_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            if prefix == '':  # First level (ticker names)
                flat_dict[k] = flatten_dict(v, '')
            else:
                flat_dict.update(flatten_dict(v, f'{prefix}{k}-'))
        else:
            flat_dict[f'{prefix}{k}'] = v
    return flat_dict

# Load the two json files
with open('indices_old.json', 'r') as f:
    old_data = json.load(f)
    old_data = {k: flatten_dict(v) for k, v in old_data.items()}

with open('indices_new.json', 'r') as f:
    new_data = json.load(f)
    new_data = {k: flatten_dict(v) for k, v in new_data.items()}

# Find the differences
diff = DeepDiff(old_data, new_data)
print(diff)

# Prepare the differences for the CSV
differences = []
if 'values_changed' in diff:
    for key_path, change in diff['values_changed'].items():
        ticker = key_path.split("'")[1]
        key = key_path.split("'")[3]
        old_value = change['old_value']
        new_value = change['new_value']
        differences.append([ticker, key, old_value, new_value])

if 'iterable_item_removed' in diff:
    for key_path in diff['iterable_item_removed']:
        parts = key_path.split("'")
        ticker = parts[1]
        key = parts[3]
        differences.append([ticker, key, 'Removed item', ''])

# Write the differences to the CSV
with open('differences.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Ticker', 'Key', 'Old Value', 'New Value'])
    writer.writerows(differences)
