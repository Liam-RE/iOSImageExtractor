# Load necessary assembly for sending keystrokes
Add-Type -AssemblyName System.Windows.Forms

# Set the path to iTunes
$iTunesPath = "C:\Program Files\iTunes\iTunes.exe"

# Start iTunes
Start-Process -FilePath $iTunesPath

