import os
import shutil
from pathlib import Path

# Extension mapping dictionary defining categories
EXTENSION_MAP = {
    # Documents
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.doc': 'Documents',
    '.txt': 'Documents',
    '.pptx': 'Documents',
    '.xlsx': 'Documents',
    '.csv': 'Documents',
    
    # Images
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.svg': 'Images',
    '.bmp': 'Images',
    
    # Videos
    '.mp4': 'Videos',
    '.mkv': 'Videos',
    '.mov': 'Videos',
    '.avi': 'Videos',
    
    # Archives
    '.zip': 'Archives',
    '.tar': 'Archives',
    '.gz': 'Archives',
    '.rar': 'Archives',
    '.7z': 'Archives',
    
    # Code & Scripts
    '.py': 'Code',
    '.js': 'Code',
    '.html': 'Code',
    '.css': 'Code',
    '.cpp': 'Code',
    '.java': 'Code',
    '.json': 'Code'
}


def get_unique_filepath(target_dir: Path, filename: str) -> Path:
    """
    Handles naming collisions by adding a numeric suffix (e.g., file_1.pdf).
    """
    path = target_dir / filename
    if not path.exists():
        return path
    
    stem = path.stem
    suffix = path.suffix
    counter = 1
    
    while True:
        new_path = target_dir / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def organize_directory(target_path: str):
    """
    Scans the target directory, categorizes files based on extension,
    relocates them securely with exception handling, and prints execution summary.
    """
    base_dir = Path(target_path).resolve()

    if not base_dir.exists() or not base_dir.is_dir():
        print(f"[Error] Provided path '{target_path}' is not a valid directory.")
        return

    stats = {
        'moved': 0,
        'errors': 0
    }

    print(f"\n==================================================")
    print(f" Organising Directory: {base_dir}")
    print(f"==================================================\n")

    try:
        # Fast directory entry iteration using os.scandir
        with os.scandir(base_dir) as entries:
            for entry in entries:
                # Process only files (ignore directories and symlinks)
                if not entry.is_file(follow_symlinks=False):
                    continue

                file_path = Path(entry.path)
                ext = file_path.suffix.lower()

                # Ignore the organizer script itself if run in the same directory
                if file_path.name == "organizer.py":
                    continue

                # Determine target folder category (default to 'Others')
                category = EXTENSION_MAP.get(ext, 'Others')
                category_dir = base_dir / category

                # Safely create folder if it doesn't exist
                category_dir.mkdir(exist_ok=True)

                # Ensure unique destination path to avoid overwriting
                target_file_path = get_unique_filepath(category_dir, file_path.name)

                try:
                    shutil.move(str(file_path), str(target_file_path))
                    print(f"[MOVED] {file_path.name}  --->  {category}/{target_file_path.name}")
                    stats['moved'] += 1

                except PermissionError:
                    print(f"[PERMISSION ERROR] Permission denied for: {file_path.name}")
                    stats['errors'] += 1
                except FileExistsError:
                    print(f"[COLLISION ERROR] Target file exists: {file_path.name}")
                    stats['errors'] += 1
                except Exception as e:
                    print(f"[ERROR] Failed to relocate {file_path.name}: {e}")
                    stats['errors'] += 1

    except Exception as e:
        print(f"[FATAL ERROR] Unable to scan directory: {e}")
        return

    # Print Formatted Execution Summary Output
    print("\n" + "="*50)
    print(" EXECUTION SUMMARY")
    print("="*50)
    print(f" Total Files Relocated : {stats['moved']}")
    print(f" Total Errors Encountered: {stats['errors']}")
    print("==================================================\n")


if __name__ == "__main__":
    folder = input("Enter path to organize (Press Enter for current directory): ").strip()
    if not folder:
        folder = "."

    organize_directory(folder)