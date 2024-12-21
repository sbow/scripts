#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path
import argparse

def is_hidden_path(path):
    """Check if any part of the path is hidden (starts with .)"""
    return any(part.startswith('.') for part in Path(path).parts)

def serialize_dir(start_path='.'):
    # Initialize the result dictionary
    result = {
        'directories': [],
        'files': [],
        'file_contents': {}
    }
    
    # Extensions to read
    target_extensions = {'.sh', '.toml', '.yml', '.py'}
    
    # Convert start_path to absolute path
    abs_start_path = os.path.abspath(start_path)
    
    # Check if directory exists
    if not os.path.exists(abs_start_path):
        raise FileNotFoundError(f"Directory not found: {start_path}")
    
    # Walk through the directory
    for root, dirs, files in os.walk(abs_start_path):
        # Remove hidden directories
        dirs[:] = [d for d in dirs if not is_hidden_path(d)]
        
        # Process current directory
        rel_path = os.path.relpath(root, abs_start_path)
        if rel_path != '.' and not is_hidden_path(rel_path):
            result['directories'].append(rel_path)
        
        # Process files
        for file in files:
            file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(file_path, abs_start_path)
            
            # Skip hidden files and files in hidden directories
            if is_hidden_path(rel_file_path):
                continue
            
            # Add to files list
            result['files'].append(rel_file_path)
            
            # Read content of target extensions
            if any(file.endswith(ext) for ext in target_extensions):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        result['file_contents'][rel_file_path] = f.read()
                except Exception as e:
                    result['file_contents'][rel_file_path] = f"Error reading file: {str(e)}"
    
    return result

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Scan directory and create JSON report of files and contents')
    parser.add_argument('scan_path', help='Relative path to directory to scan')
    parser.add_argument('output_file', help='Name of the output JSON file')
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Scan the directory
        result = serialize_dir(args.scan_path)
        
        # Write to JSON file in current directory
        output_path = os.path.join(os.getcwd(), args.output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        
        print(f"Scan complete! Results written to {output_path}")
        print(f"Found {len(result['directories'])} directories and {len(result['files'])} files")
        print(f"Read contents of {len(result['file_contents'])} files")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
