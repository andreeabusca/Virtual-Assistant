from fpdf import FPDF
from PIL import Image
import os
from speak import speak 

def images_to_pdf(image_folder, output_folder, output_pdf_name):
     
    images = []

    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all image files from the folder
    for file_name in sorted(os.listdir(image_folder)):  # Sort for consistent order
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(image_folder, file_name)
            img = Image.open(img_path)
            # Convert all images to RGB mode (required for PDF)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)

    if images:
        # Create the full path for the output PDF
        output_pdf_path = os.path.join(output_folder, output_pdf_name)
        
        # Save all images into a single PDF
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
        print(f"PDF saved successfully")
        speak(f"PDF saved successfully")
    else:
        print("No images found in the folder.")
        speak("No images found in the folder.")

    