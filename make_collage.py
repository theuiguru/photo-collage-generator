import os
import math
from PIL import Image

def make_collage(image_folder, output_path="collage_output.jpg", cell_size=(350, 350), padding=8):
    # Supported file formats
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    # Get all image paths from the folder
    if not os.path.exists(image_folder):
        print(f"Error: Folder '{image_folder}' not found!")
        return
        
    image_files = [
        os.path.join(image_folder, f) for f in os.listdir(image_folder)
        if f.lower().endswith(valid_extensions)
    ]
    
    num_images = len(image_files)
    if num_images == 0:
        print(f"No valid images found in '{image_folder}'!")
        return

    print(f"Found {num_images} photos in '{image_folder}'. Generating grid layout...")

    # Calculate rows and columns dynamically based on total image count
    cols = math.ceil(math.sqrt(num_images))
    rows = math.ceil(num_images / cols)

    # Calculate overall dimensions
    grid_width = cols * cell_size[0] + (cols + 1) * padding
    grid_height = rows * cell_size[1] + (rows + 1) * padding

    # Create canvas with a clean dark slate background
    collage = Image.new('RGB', (grid_width, grid_height), color=(30, 30, 30))

    for idx, img_path in enumerate(image_files):
        row = idx // cols
        col = idx % cols
        
        x = padding + col * (cell_size[0] + padding)
        y = padding + row * (cell_size[1] + padding)
        
        try:
            with Image.open(img_path) as img:
                # Crop and resize to uniform square cells without distortion
                img_ratio = img.width / img.height
                target_ratio = cell_size[0] / cell_size[1]

                if img_ratio > target_ratio:
                    new_width = int(img.height * target_ratio)
                    offset = (img.width - new_width) // 2
                    img = img.crop((offset, 0, offset + new_width, img.height))
                else:
                    new_height = int(img.width / target_ratio)
                    offset = (img.height - new_height) // 2
                    img = img.crop((0, offset, img.width, offset + new_height))

                img = img.resize(cell_size, Image.Resampling.LANCZOS)
                collage.paste(img, (x, y))
        except Exception as e:
            print(f"Skipping {img_path}: {e}")

    collage.save(output_path, quality=95)
    print(f"Success! Collage saved as '{output_path}'.")

if __name__ == "__main__":
    # Change './photos' to match your target folder path
    FOLDER_PATH = "./photos" 
    make_collage(image_folder=FOLDER_PATH, output_path="collage_output.jpg")