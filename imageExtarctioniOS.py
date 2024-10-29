import sqlite3
import os
from shutil import copyfile

# https://github.com/bsdtrhodes/itunes-backup-extractor/blob/main/itunes-img-extractor.py (modified to work in this project).
def ImageExtraction(ManifestPath, BackupDir, OutputDir):
    # Connect to db
    try:
        conn = sqlite3.connect(ManifestPath)
    except sqlite3.Error as e:
        print("Error connecting to the database:", e)
        exit()

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Select files from the CameraRollDomain with specific extensions
    cursor.execute("SELECT fileID, relativePath FROM Files WHERE domain = 'CameraRollDomain' AND (relativePath LIKE '%.jpg' OR relativePath LIKE '%.heic' OR relativePath LIKE '%.png' OR relativePath LIKE '%.mov' OR relativePath LIKE '%.mp4' OR relativePath LIKE '%.gif')")
    rows = cursor.fetchall()

    for row in rows:
        id = row["fileID"]
        RelativePath = row["relativePath"]
        
        if not id:
            continue

        fileDirectory = id[:2]
        source = os.path.join(BackupDir, fileDirectory, id)
        # Copies files to selected path      
        destinationPath = os.path.join(OutputDir, os.path.basename(RelativePath))
        os.makedirs(os.path.dirname(destinationPath), exist_ok=True)

        # Check if the item is a file
        if os.path.isfile(source):
            # Check if the file has one of the specified extensions
            if any(RelativePath.lower().endswith(ext) for ext in ['.jpg', '.heic', '.png', '.mov', '.mp4', '.gif']):
                print(f"Copying {source} to {destinationPath}")
                copyfile(source, destinationPath)

    cursor.close()
    conn.close()
