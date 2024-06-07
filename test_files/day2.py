import os
import itertools
from Levenshtein import distance
import pandas as pd

def list_files_recursive(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(root, filename), directory))
    return files

def find_related_files(folders):
    related_files = {os.path.basename(folder): [] for folder in folders}

    for folder1, folder2 in itertools.combinations(folders, 2):
        try:
            files1 = list_files_recursive(folder1)
        except OSError as e:
            print(f"Error accessing folder {folder1}: {e}")
            continue

        try:
            files2 = list_files_recursive(folder2)
        except OSError as e:
            print(f"Error accessing folder {folder2}: {e}")
            continue

        for file1 in files1:
            for file2 in files2:
                # Calculate Levenshtein distance between file names
                dist = distance(file1.lower(), file2.lower())
                # Adjust the threshold as needed
                if dist < 10:  # Adjust the threshold as needed
                    related_files[os.path.basename(folder1)].append(file1)
                    related_files[os.path.basename(folder2)].append(file2)

    # Find the maximum length among all lists
    max_length = max(len(files) for files in related_files.values())
    # Pad each list with empty strings to match the maximum length
    for files in related_files.values():
        files.extend([''] * (max_length - len(files)))

    return related_files

# Specify the folders you want to compare
folders = [
    'C:/xampp/htdocs/migration_campus/RDF_BF',
    'C:/xampp/htdocs/migration_campus/RDF_BVO',
    'C:/xampp/htdocs/migration_campus/RDF_JSON',
    'C:/xampp/htdocs/migration_campus/RDF_JS_OBJ',
    'C:/xampp/htdocs/migration_campus/RDF_UI'
]

related_files = find_related_files(folders)

# Create a DataFrame with folders as columns and related files as rows
df = pd.DataFrame(related_files)

# Transpose the DataFrame to have folders as rows and related files as columns

# Save the DataFrame as an Excel file
df.to_excel('related_files.xlsx')
