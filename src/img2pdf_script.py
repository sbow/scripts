import img2pdf
import sys
import os
from pathlib import Path

def convert_images_to_pdf(input_path, output_pdf):
    # Ensure the input path is a directory
    if not os.path.isdir(input_path):
        print(f"Error: {input_path} is not a valid directory.")
        sys.exit(1)

    # Get all jpg files in the directory
    jpg_files = [f for f in os.listdir(input_path) if f.lower().endswith('.jpg')]
    
    # If no jpg files are found
    if not jpg_files:
        print(f"No JPG files found in the directory: {input_path}")
        sys.exit(1)
    
    # Create full paths for each image file
    image_paths = [os.path.join(input_path, f) for f in jpg_files]
    
    # Convert the images to PDF using im2pdf
    try:
        with open(output_pdf, "wb") as output_file:
            output_file.write(img2pdf.convert(image_paths))
        print(f"PDF generated successfully: {output_pdf}")
    except Exception as e:
        print(f"Error during PDF creation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python im2pdf_script.py <input_folder_path> <output_pdf_path>")
        sys.exit(1)
    
    input_folder = sys.argv[1]  # Path to the folder containing jpg images
    output_pdf = sys.argv[2]    # Path to save the output PDF
    
    convert_images_to_pdf(input_folder, output_pdf)

