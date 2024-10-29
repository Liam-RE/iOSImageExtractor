import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import os
import subprocess
from shutil import copyfile
import glob
import datetime

# Function to get the most recent backup folder
def LatestiTunesBackup():
    BasePath = os.path.expanduser(r'~\AppData\Roaming\Apple Computer\MobileSync\Backup')
    # Get a list of all backup folders
    BackupFolders = glob.glob(os.path.join(BasePath, '*'))

    # Check if there are any backup folders
    if not BackupFolders:
        return None

    # Find the most recent folder based on last modified time
    LatestBackup = max(BackupFolders, key=os.path.getmtime)
    return LatestBackup

# Function to handle image extraction
def ImageExtraction(ManifestPath, BackupDir, OutputDir):
    try:
        conn = sqlite3.connect(ManifestPath)
    except sqlite3.Error as e:
        print("Error connecting to the database:", e)
        messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
        return

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT fileID, relativePath FROM Files WHERE domain = 'CameraRollDomain' AND "
                   "(relativePath LIKE '%.jpg' OR relativePath LIKE '%.heic' OR relativePath LIKE '%.png' "
                   "OR relativePath LIKE '%.mov' OR relativePath LIKE '%.mp4' OR relativePath LIKE '%.gif')")
    rows = cursor.fetchall()

    for row in rows:
        id = row["fileID"]
        RelativePath = row["relativePath"]
        
        if not id:
            continue

        fileDirectory = id[:2]
        source = os.path.join(BackupDir, fileDirectory, id)
        destinationPath = os.path.join(OutputDir, os.path.basename(RelativePath))
        os.makedirs(os.path.dirname(destinationPath), exist_ok=True)

        if os.path.isfile(source):
            if any(RelativePath.lower().endswith(ext) for ext in ['.jpg', '.heic', '.png', '.mov', '.mp4', '.gif']):
                print(f"Copying {source} to {destinationPath}")
                copyfile(source, destinationPath)

    cursor.close()
    conn.close()
    messagebox.showinfo("Completed", "Image extraction completed successfully!")

# GUI setup
def SelectOutput():
    output_path.set(filedialog.askdirectory(title="Select Output Directory"))

def StartExtraction():
    latest_backup = LatestiTunesBackup()
    if not latest_backup:
        messagebox.showerror("Backup Error", "No backup folders found.")
        return

    manifest_path.set(os.path.join(latest_backup, 'Manifest.db'))
    backup_path.set(latest_backup)

    if not output_path.get():
        messagebox.showwarning("Input Error", "Please select the output directory.")
        return
    ImageExtraction(manifest_path.get(), backup_path.get(), output_path.get())

def StopExtraction():
    global is_running
    is_running = False


def Notification(title, message):
    messagebox.showinfo(title, message)

def RuniTunes():
    iTunesPath = r"C:\Program Files\iTunes\iTunes.exe"

    try:
        # Start iTunes in the background
        subprocess.Popen([iTunesPath])

        # Display the message immediately
        Notification("Backup Needed", "Please backup iDevice using iTunes. Once complete, select the directory for the images to be placed and Start Extraction.")

    except FileNotFoundError:
        messagebox.showerror("Error", "iTunes executable not found. Please check the path.")

# Initialize GUI window
root = tk.Tk()
root.title("iOS Image Extractor")

manifest_path = tk.StringVar()
backup_path = tk.StringVar()
output_path = tk.StringVar()
root.resizable(False, False) 

# Create GUI elements
tk.Label(root, text="Start iTunes:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Button(root, text="Start", command=RuniTunes).grid(row=0, column=1, padx=12, pady=12)

tk.Label(root, text="Output Directory:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
tk.Entry(root, textvariable=output_path, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=SelectOutput).grid(row=1, column=2, padx=12, pady=12)
button_width = 15 


tk.Button(root, text="Start Extraction", command=StartExtraction, bg="green").grid(row=3, column=1, padx=(10, 5), pady=10, sticky="ew")  
tk.Button(root, text="Stop Extraction", command=StopExtraction, bg="red").grid(row=4, column=1, padx=(10, 5), pady=10, sticky="ew")  

# Run the GUI loop
root.mainloop()
