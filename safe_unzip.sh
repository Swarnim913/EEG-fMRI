#!/bin/bash

# Check if filename is provided
if [ -z "$1" ]; then
  echo "Usage: $0 filename.zip"
  exit 1
fi

# Get the zip filename from the first argument
zipfile=$1

# Create a temporary extraction folder
tempdir=$(mktemp -d)

# Check if unzip is installed
if ! command -v unzip &> /dev/null; then
    echo "unzip command not found. Please install unzip first."
    exit 1
fi

# List all files in the zip archive, handle special characters
files=$(unzip -Z1 "$zipfile")

# Extract and remove each file one by one
while IFS= read -r file; do
    echo "Extracting '$file' ..."
    
    # Extract the file, use quotes to handle spaces and special characters
    unzip -j "$zipfile" "$file" -d "$tempdir"
    
    # Check if the extraction was successful
    if [ $? -eq 0 ]; then
        echo "File '$file' extracted. Deleting it from the archive..."
        
        # Remove the file from the archive, use quotes to handle spaces and special characters
        zip -d "$zipfile" "$file" > /dev/null
    else
        echo "Error extracting '$file'."
    fi
done <<< "$files"

# Move extracted files to current directory
if [ -n "$(ls -A "$tempdir")" ]; then
    mv "$tempdir"/* .
else
    echo "No files were extracted."
fi

# Clean up temporary directory
rm -r "$tempdir"

echo "Unzipping complete and original zip file has been reduced!"