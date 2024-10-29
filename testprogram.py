import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import os
from shutil import copyfile

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
def select_manifest():
    manifest_path.set(filedialog.askopenfilename(title="Select Manifest.db", filetypes=[("Database Files", "*.db")]))
    
def select_backup():
    backup_path.set(filedialog.askdirectory(title="Select Backup Directory"))

def select_output():
    output_path.set(filedialog.askdirectory(title="Select Output Directory"))

def run_extraction():
    if not manifest_path.get() or not backup_path.get() or not output_path.get():
        messagebox.showwarning("Input Error", "Please select all necessary paths.")
        return
    ImageExtraction(manifest_path.get(), backup_path.get(), output_path.get())

# Initialize GUI window
root = tk.Tk()
root.title("iOS Image Extractor")

# Variables to hold file paths
manifest_path = tk.StringVar()
backup_path = tk.StringVar()
output_path = tk.StringVar()

# Create GUI elements
tk.Label(root, text="Manifest.db Path:").grid(row=0, column=0, sticky="w")
tk.Entry(root, textvariable=manifest_path, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=select_manifest).grid(row=0, column=2)

tk.Label(root, text="Backup Directory:").grid(row=1, column=0, sticky="w")
tk.Entry(root, textvariable=backup_path, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=select_backup).grid(row=1, column=2)

tk.Label(root, text="Output Directory:").grid(row=2, column=0, sticky="w")
tk.Entry(root, textvariable=output_path, width=50).grid(row=2, column=1)
tk.Button(root, text="Browse", command=select_output).grid(row=2, column=2)

tk.Button(root, text="Start Extraction", command=run_extraction, bg="lightblue").grid(row=3, column=0, columnspan=3, pady=10)

# Run the GUI loop
root.mainloop()
