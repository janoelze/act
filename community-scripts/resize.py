# /// script
# command = "resize"
# description = "Resizes the images in the current directory to a specified width"
# aliases = ["resize"]
# author = "janoelze"
# dependencies = [
#   "Pillow"
# ]
# ///

import sys
import os
import argparse
import concurrent.futures
from PIL import Image

def resize_image(path, width):
    ###
    # Resize the image at the given path to the specified width.
    # * Maintains the aspect ratio.
    # * Saved the resized image to the same path, but appends "-$width" to the filename.
    ###
    img = Image.open(path)
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((width, hsize), Image.ANTIALIAS)
    new_path = f"{os.path.splitext(path)[0]}-{width}{os.path.splitext(path)[1]}"
    img.save(new_path)
    return new_path

def resize_images(directory, width):
    # Scan the directory and separate image files and subdirectories
    image_files = []
    subdirs = []
    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_file() and entry.name.lower().endswith((".jpg", ".jpeg", ".png")):
                image_files.append(entry.path)
            elif entry.is_dir():
                subdirs.append(entry.path)

    # Only start threads if there are any image files to resize
    if len(image_files) > 0:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(resize_image, path, width) for path in image_files]
            for future in concurrent.futures.as_completed(futures):
                try:
                    print(f"Resized: {future.result()}")
                except Exception as e:
                    print(f"Error: {e}")
    else:
        print("No image files found to resize")

def main():
    parser = argparse.ArgumentParser(description="Resizes the images in the current directory to a specified width")
    parser.add_argument("width", type=int, help="The width to resize the images to")
    args = parser.parse_args()

    # check if the width is valid
    if args.width <= 0:
        print("Error: Invalid width")
        sys.exit(1)

    resize_images(os.getcwd(), args.width)

if __name__ == "__main__":
    main()