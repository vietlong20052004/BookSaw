import os
from PIL import Image


def resize_images_in_folder(input_folder, output_folder, target_size):
    """
    Resize all images in the input folder and save them to the output folder.

    Parameters:
        input_folder (str): Path to the folder containing original images
        output_folder (str): Path to save resized images
        target_size (tuple): Desired size as (width, height) in pixels
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Supported image file extensions
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')

    # Process each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            try:
                # Open the image file
                img_path = os.path.join(input_folder, filename)
                img = Image.open(img_path)

                # Resize the image
                resized_img = img.resize(target_size, Image.LANCZOS)

                # Save the resized image
                output_path = os.path.join(output_folder, filename)
                resized_img.save(output_path)

                print(f"Resized {filename} to {target_size}")

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")


if __name__ == "__main__":
    # User configuration
    input_folder = "media/book_covers3"  # Replace with your input folder path
    output_folder = "media/book_covers"  # Replace with your output folder path
    target_width = 150  # Desired width in pixels
    target_height = 230  # Desired height in pixels

    # Resize all images
    resize_images_in_folder(input_folder, output_folder, (target_width, target_height))