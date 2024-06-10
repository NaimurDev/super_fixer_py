import os
import random
from PIL import Image, ImageOps
from tqdm import tqdm

# Define the directories
typo_groups_dir = 'typo-groups'
midjourney_images_dir = 'midjourney-1600-images'
output_dir = 'output'
frame_filename = 'frame.png'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the frame image
frame = Image.open(frame_filename)

# Get the dimensions of the frame
frame_width, frame_height = frame.size

# List and shuffle directories in typo-groups
typo_groups_dirs = [os.path.join(typo_groups_dir, d) for d in os.listdir(typo_groups_dir) if os.path.isdir(os.path.join(typo_groups_dir, d))]
random.shuffle(typo_groups_dirs)

# List and shuffle images in midjourney-1600-images
midjourney_images = [os.path.join(midjourney_images_dir, f) for f in os.listdir(midjourney_images_dir) if f.endswith('.png')]
random.shuffle(midjourney_images)

typo_groups_dirs_original = typo_groups_dirs.copy()
midjourney_images_original = midjourney_images.copy()


def generate_images(num_images):
    global typo_groups_dirs, midjourney_images
    
    for i in tqdm(range(num_images)):

        if typo_groups_dirs == []:
            typo_groups_dirs = typo_groups_dirs_original.copy()
            random.shuffle(typo_groups_dirs)
        
        if midjourney_images == []:
            midjourney_images = midjourney_images_original.copy()
            random.shuffle(midjourney_images)

        # Pop one folder from the shuffled typo-groups array
        typograph_dir = typo_groups_dirs.pop() if typo_groups_dirs else random.choice(typo_groups_dirs)
        
        # Pop one background image from the shuffled midjourney images array
        background_filename = midjourney_images.pop() if midjourney_images else random.choice(midjourney_images)
        
        # Select a random typography image from the typograph_dir
        typograph_filename = random.choice([os.path.join(typograph_dir, f) for f in os.listdir(typograph_dir) if f.endswith('.png')])
        
        # Construct the output filename
        bgname = os.path.basename(background_filename).split('.')[0]
        dirname = typograph_dir.split('/')[-1]
        typoname = os.path.basename(typograph_filename).split('.')[0]
        typoname = str(int(os.path.basename(typograph_filename).split('.')[0]) % 30 or 30)
        output_filename = os.path.join(output_dir, f'{dirname}_{typoname}_{bgname}.png')
        
        # Open the images
        background = Image.open(background_filename)
        typograph = Image.open(typograph_filename)
        
        # Create a blank canvas with the same dimensions as the frame
        canvas = Image.new('RGBA', (frame_width, frame_height), (255, 255, 255, 0))

        # Resize the background to fit the canvas without stretching
        frame_aspect_ratio = frame_width / frame_height
        background_aspect_ratio = background.width / background.height

        # Resize the background image to cover the frame while maintaining the aspect ratio
        if frame_aspect_ratio > background_aspect_ratio:
            # Frame is wider than the background
            new_height = int(frame_width * 1.5)
            new_width = int(new_height * background_aspect_ratio)
        else:
            # Frame is taller than the background
            new_width = frame_height
            new_height = int(new_width / background_aspect_ratio)

        background = background.resize((new_width, new_height), Image.LANCZOS)
        
        # Calculate the position to paste the background on the canvas to center it
        x_offset = (frame_width - new_width) // 2
        y_offset = (frame_height - new_height) // 2

        # Paste the background onto the canvas
        canvas.paste(background, (x_offset, y_offset))

        # Trim the typography image using its bounding box
        typograph = typograph.crop(typograph.getbbox())

        # Determine the resizing ratio based on the area of the trimmed typography image
                
        if typograph.height > typograph.width:
            # Typograph height is more than its width
            new_typo_height = int(frame_height * 0.75)
            new_typo_width = int(new_typo_height * (typograph.width / typograph.height))
        else:
            # Typograph width is more than its height
            new_typo_width = int(frame_width * 0.75)
            new_typo_height = int(new_typo_width * (typograph.height / typograph.width))
    

        typograph = typograph.resize((new_typo_width, new_typo_height), Image.LANCZOS)

        # Calculate the position to paste the typography on the canvas to center it
        typo_x_offset = (frame_width - new_typo_width) // 2
        typo_y_offset = (frame_height - new_typo_height) // 2

        # Paste the typography onto the canvas
        canvas.alpha_composite(typograph, (typo_x_offset, typo_y_offset))

        # Paste the original frame on top
        canvas.alpha_composite(frame)

        # Save the combined image
        canvas.save(output_filename, format='PNG')

    print(f"{num_images} images combined and saved successfully.")

# Call the generate_images function with the desired number of images
def main():
    print("How many images to generate?")
    num_images = int(input())
    generate_images(num_images)

if __name__ == '__main__':
    main()
