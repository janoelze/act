#!/usr/bin/env python3
# /// script
# command = "tomp4"
# description = "Convert any video format to a web-ready MP4 with small file size and reasonable resolution"
# aliases = ["tomp4"]
# author = "janoelze"
# dependencies = []
# ///

import os
import sys
import subprocess

def main():
    if len(sys.argv) != 2:
        print("Usage: tomp4 <input_video>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.isfile(input_file):
        print("Error: File does not exist.")
        sys.exit(1)
    
    # Determine output file path.
    # This script appends "_web.mp4" to the input file's base name.
    input_dir = os.path.dirname(input_file)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(input_dir, f"{base_name}_web.mp4")
    
    # Build the ffmpeg command:
    # - The video filter scales the video to a maximum width of 1280 and maximum height of 720,
    #   preserving aspect ratio by decreasing dimensions if necessary.
    # - The video codec is libx264 with a "slow" preset and a CRF value of 28 for a balance between quality and file size.
    # - The audio codec is AAC at 128 kbps.
    cmd = [
        "ffmpeg", "-i", input_file,
        "-vf", "scale='min(1280,iw)':'min(720,ih)':force_original_aspect_ratio=decrease",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "28",
        "-c:a", "aac",
        "-b:a", "128k",
        output_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to convert the video to a web-ready MP4.")
        sys.exit(1)
    
    print("Conversion successful. Output file is:", output_file)

if __name__ == "__main__":
    main()
