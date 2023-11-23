import json
import csv
import os


def convert_folder_to_csv(folder_path, output_csv):
    with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
        fieldnames = ["pregunta", "respuesta"]  # Field names in lowercase
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC
        )

        writer.writeheader()
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                json_file_path = os.path.join(folder_path, filename)
                with open(json_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    num_rows = len(data)
                    print(f"File: {filename}, Rows: {num_rows}")
                    for row_num, item in enumerate(data, start=1):
                        # Ensure that keys are in lowercase and match the field names in CSV
                        item_dict = {}
                        for field in fieldnames:
                            key = field.lower()
                            value = item.get(field, "")
                            if field == "respuesta":
                                value = (
                                    value.strip()
                                )  # Remove leading/trailing whitespaces
                            item_dict[key] = value
                        writer.writerow(item_dict)


# Specify your folder path containing JSON files and the output CSV file
folder_path = "data/"
output_csv = "tesis_dataset.csv"

# Convert all JSON files in the folder to a single CSV file
convert_folder_to_csv(folder_path, output_csv)
