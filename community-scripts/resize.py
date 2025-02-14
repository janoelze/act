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
import glob

def resize_image(path, width):
    img = Image.open(path)
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((width, hsize), Image.Resampling.LANCZOS)
    new_path = f"{os.path.splitext(path)[0]}-w{width}{os.path.splitext(path)[1]}"
    img.save(new_path)
    return new_path

def resize_images(paths, width):
    image_files = [p for p in paths if p.lower().endswith((".jpg", ".jpeg", ".png"))]

    if image_files:
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
    parser = argparse.ArgumentParser(description="Resize images to a specified width with glob support.")
    parser.add_argument("width", type=int, help="The width to resize the images to")
    parser.add_argument("path", nargs='?', default=os.getcwd(), help="Directory or file pattern to resize (supports glob)")
    args = parser.parse_args()

    if args.width <= 0:
        print("Error: Invalid width")
        sys.exit(1)

    paths = []

    if os.path.isdir(args.path):
        paths = glob.glob(os.path.join(args.path, "**", "*.*"), recursive=True)
    else:
        paths = glob.glob(args.path)

    resize_images(paths, args.width)

if __name__ == "__main__":
    main()