
# iOS Image Extractor

iOS Image Extractor is a Windows-based GUI application built with Python and Tkinter, designed to simplify the process of extracting images and videos from an iOS device backup. This program locates and extracts image and video files (e.g., `.jpg`, `.heic`, `.png`, `.mov`, `.mp4`, and `.gif`) from the latest iTunes backup on your system.

## Features

- Automatically identifies the latest iTunes backup folder on the system.
- Extracts images and videos from the `CameraRollDomain` section of the iOS backup.
- Provides a simple, user-friendly GUI for easy operation.
- Option to start iTunes for creating a new backup if necessary.
- **Executable File**: A standalone executable file (.exe) is provided for easy execution without needing Python installed.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Tkinter** (usually included with Python installations)
- **iTunes** - Required to create iOS backups on Windows. [Download here](https://www.apple.com/itunes/download/)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Liam-RE/iPhoneImageExtractor
## Usage

### Extract Images:
- Click "Start" to launch iTunes if you need to create a new backup.
- Once your backup is created, click "Browse" to select the output directory where extracted images should be saved.
- Click "Start Extraction" to begin extracting images and videos to the chosen folder.
- To stop the extraction process, click "Stop Extraction".





## Troubleshooting
- **File Locations**: This Program assumes that iTunes and your backup data are saved to the **defaut** location in Windows.

