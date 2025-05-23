import json
import csv

def json_to_csv(input_filename, output_filename='emil2.csv'):
    try:
        with open(input_filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of objects.")

        with open(output_filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f"Successfully converted {input_filename} to {output_filename}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
json_to_csv('2025-04-23_01-28-32\emildardak_comments.json')
