import os
import itertools
from Levenshtein import distance

def find_related_files(folders):
    related_files = []

    for folder1, folder2 in itertools.combinations(folders, 2):
        try:
            files1 = os.listdir(folder1)
        except OSError as e:
            print(f"Error accessing folder {folder1}: {e}")
            continue

        try:
            files2 = os.listdir(folder2)
        except OSError as e:
            print(f"Error accessing folder {folder2}: {e}")
            continue

        for file1 in files1:
            for file2 in files2:
                # Calculate Levenshtein distance between file names
                dist = distance(file1.lower(), file2.lower())
                # Adjust the threshold as needed
                if dist < 5:  # Adjust the threshold as needed
                    related_files.append((file1, file2))

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
if related_files:
    for file_pair in related_files:
        print(f"Related files: {file_pair[0]} - {file_pair[1]}")
else:
    print("No related files found.")
