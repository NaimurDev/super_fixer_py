# image_enhancer % python pillow_enhancer.py images output --sharpness_factor 3.0 --contrast_factor 2.5 --brightness_factor 1.2

from PIL import Image, ImageEnhance
import os

def enhance_image(image_path, output_path, sharpness_factor=2.0, contrast_factor=1.5, brightness_factor=1.2):
    # Open an image file
    with Image.open(image_path) as img:
        # Enhance sharpness
        sharpness_enhancer = ImageEnhance.Sharpness(img)
        img = sharpness_enhancer.enhance(sharpness_factor)
        
        # Enhance contrast
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(contrast_factor)
        
        # Enhance brightness
        brightness_enhancer = ImageEnhance.Brightness(img)
        img = brightness_enhancer.enhance(brightness_factor)
        
        # Save the modified image
        img.save(output_path)

def process_images(input_folder, output_folder, sharpness_factor=2.0, contrast_factor=1.5, brightness_factor=1.2):
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Process all images in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            enhance_image(input_path, output_path, sharpness_factor, contrast_factor, brightness_factor)
            print(f'Processed {filename}')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Enhance the crispness of images.')
    parser.add_argument('input_folder', type=str, help='The folder containing input images.')
    parser.add_argument('output_folder', type=str, help='The folder to save enhanced images.')
    parser.add_argument('--sharpness_factor', type=float, default=2.0, help='Factor to enhance sharpness. Default is 2.0')
    parser.add_argument('--contrast_factor', type=float, default=1.5, help='Factor to enhance contrast. Default is 1.5')
    parser.add_argument('--brightness_factor', type=float, default=1.2, help='Factor to enhance brightness. Default is 1.2')

    args = parser.parse_args()

    process_images(args.input_folder, args.output_folder, args.sharpness_factor, args.contrast_factor, args.brightness_factor)
