import os
import json
from PIL import Image
import pandas as pd
from natsort import natsorted
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
import random

csv_file_path = 'quotes.csv'
directory = 'images'
num_images = 100
df = pd.read_csv(csv_file_path)
all_usd_images = []
book_no = 1
size_increase = -1

# Set the size of the PDF page
page_width, page_height = letter
page_width /= inch  # convert to inches
page_height /= inch  # convert to inches

used_images = []

# Function to resize the image while maintaining aspect ratio and adding 1 cm extra border
def resize_image(image, max_width, max_height):
    max_width += size_increase * cm / inch  # Increase by size_increase cm
    max_height += size_increase * cm / inch  # Increase by size_increase cm
    width, height = image.size
    if width > max_width or height > max_height:
        # Calculate the new size maintaining the aspect ratio
        ratio = min(max_width / width, max_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.LANCZOS)
    return image

def create_book(book_no, folder_images):
    image_added = 0
    this_used_text = []
    this_used_background = []
    folder_names = random.shuffle(list(folder_images.keys()))
    
    while image_added < num_images:
        for folder_name in folder_names:
            if folder_and_used_data[folder_name]['image_point'] < folder_and_used_data[folder_name]['length']:
                if folder_name in selected_folder_names:
                    continue
                img = folder_images[folder_name][folder_and_used_data[folder_name]['image_point']]
                combined_images.append(img)
                all_usd_images.append(img)
                this_book_used_images.append(img)
                selected_folder_names.append(folder_name)
                selected_folder_indexes.append(int(folder_name) - 1)

                folder_and_used_data[folder_name]['used_images'].append(img)
                folder_and_used_data[folder_name]['image_point'] += 1
                image_added += 1
                if image_added >= num_images:
                    break

    # Create directory for the book
    book_dir = f'books/{book_no}'
    os.makedirs(book_dir, exist_ok=True)

    output_pdf = f"{book_dir}/book.pdf"
    c = canvas.Canvas(output_pdf, pagesize=letter)

    for i, img_path in enumerate(combined_images):
        img = Image.open(img_path).convert('RGB')
        
        img = resize_image(img, page_width * inch, page_height * inch)
        
        temp_img_path = f"temp_img_{i}.jpg"
        img.save(temp_img_path)

        img_width, img_height = img.size

        # Calculate the position to center the image and trim 1 cm border
        x = (page_width * inch - img_width + size_increase * cm) / 2
        y = (page_height * inch - img_height + size_increase * cm) / 2
        c.drawImage(temp_img_path, x, y, width=img_width - size_increase * cm, height=img_height - size_increase * cm)
        os.remove(temp_img_path)

        c.showPage()

    c.save()

    # Save the first five screenshots
    screenshots_dir = os.path.join(book_dir, 'screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)

    for i, image in enumerate(combined_images[:9]):
        if i % 2 == 1:
            continue
        screenshot_path = os.path.join(screenshots_dir, f'screenshot_{i+1}.png')
        Image.open(image).convert('RGB').save(screenshot_path)

    # Write the JSON
    json.dump(this_book_used_images, open(f"{book_dir}/used_filenames.json", 'w'))

    # Write the CSV
    selected_rows = df.iloc[selected_folder_indexes]
    selected_rows.to_csv(f"{book_dir}/used_quotes.csv", index=False)

    total_images = sum([data['length'] for data in folder_and_used_data.values()])
    used_images = sum([data['image_point'] for data in folder_and_used_data.values()])
    used_percentage = (used_images / total_images) * 100
    images_left = total_images - used_images

    print("-----------------")
    print(f"Book number: {book_no}")
    print(f"Total images: {total_images}")
    print(f"Images used: {used_images}")
    print(f"Used percentage: {used_percentage:.2f}%")
    print(f"Images left: {images_left}")

def main():
    global book_no

    directory_images = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    directory_images = natsorted(directory_images)
    
    folder_images = {}
    for img in directory_images:
        folder_name = os.path.basename(img).split('_')[0]
        if folder_name not in folder_images:
            folder_images[folder_name] = []
        folder_images[folder_name].append(img)
    folder_images = {k: natsorted(v) for k, v in folder_images.items()}
    
    for i in range(0, 50):
        create_book(i+1, folder_images)

if __name__ == '__main__':
    main()
