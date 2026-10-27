Automated File Organizer & Cleanup Utility

An autonomous Python desktop automation tool that scans messy folders, categorizes files into clean subdirectories (/Documents, /Images, /Videos, /Archives, /Code, /Others), handles naming collisions, and catches access permissions safely.

Features Included

Fast File Iteration: Powered by os.scandir() for maximum performance.

Smart Extension Categorization: Pre-configured mapping dictionary for all popular extensions.

Collision Safety: Automatically appends numeric increments (_1, _2) if a file with the same name already exists in the destination.

Robust Error Catching: Built-in try-except blocks handling PermissionError and FileExistsError.

Formatted Output: Prints real-time relocation logs and a structured Execution Summary.

How to Run

Place organizer.py in your target folder or run it from any terminal prompt.

Run the script:

python organizer.py


Enter the folder path you wish to organize (or press Enter to clean the current directory).
