# python main.py images output --sharpness_factor 1.5 --contrast_factor 1.5 --brightness_factor 1.2

import cv2
import os
import numpy as np

def enhance_image(image_path, output_path, sharpness_factor=1.5, contrast_factor=1.5, brightness_factor=1.2):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to float32 for accurate processing
    img = img.astype(np.float32)
    
    # Apply sharpness
    kernel = np.array([[0, -1, 0], [-1, 5 * sharpness_factor, -1], [0, -1, 0]])
    img = cv2.filter2D(img, -1, kernel)
    
    # Apply contrast and brightness adjustments
    img = cv2.convertScaleAbs(img, alpha=contrast_factor, beta=(brightness_factor - 1) * 100)
    
    # Clip the values to ensure they fall within the valid range
    img = np.clip(img, 0, 255).astype(np.uint8)
    
    # Save the enhanced image
    cv2.imwrite(output_path, img)

def process_images(input_folder, output_folder, sharpness_factor=1.5, contrast_factor=1.5, brightness_factor=1.2):
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
    parser.add_argument('--sharpness_factor', type=float, default=1.5, help='Factor to enhance sharpness. Default is 1.5')
    parser.add_argument('--contrast_factor', type=float, default=1.5, help='Factor to enhance contrast. Default is 1.5')
    parser.add_argument('--brightness_factor', type=float, default=1.2, help='Factor to enhance brightness. Default is 1.2')

    args = parser.parse_args()

    process_images(args.input_folder, args.output_folder, args.sharpness_factor, args.contrast_factor, args.brightness_factor)
