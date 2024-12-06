import os
import sys
import argparse
from datetime import datetime
import glob

def rename_files(prefix, append_date, pattern):
    # Get the current date in YYYYMMDD format
    current_date = datetime.now().strftime("%Y%m%d") if append_date else ""

    # Use glob to match files based on the provided pattern
    files = glob.glob(pattern)

    if not files:
        print(f"No files matching pattern '{pattern}' found.")
        return

    for file in files:
        # Create the new filename
        new_name = f"{current_date}_{prefix}_{os.path.basename(file)}" if append_date else f"{prefix}_{os.path.basename(file)}"

        # Rename the file
        try:
            os.rename(file, new_name)
            print(f"Renamed: {file} -> {new_name}")
        except Exception as e:
            print(f"Error renaming {file}: {e}")

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Rename files by adding a prefix and optionally a date.")
    
    # Prefix argument
    parser.add_argument("-prefix", required=True, help="Prefix to add to the files.")
    
    # Date argument (optional)
    parser.add_argument("-date", action="store_true", help="Append current date (YYYYMMDD) to the filename.")

    # File pattern argument
    parser.add_argument("pattern", help="Pattern to match the files (e.g., '*.pdf', '*.jpg', etc.).")

    args = parser.parse_args()

    # Call the rename_files function with parsed arguments
    rename_files(args.prefix, args.date, args.pattern)

if __name__ == "__main__":
    main()

