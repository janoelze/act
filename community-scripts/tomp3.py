#!/usr/bin/env python3
# /// script
# command = "tomp3"
# description = "Convert any file format to an MP3 using ffmpeg"
# aliases = ["tomp3", "to-mp3", "convert-to-mp3"]
# author = "janoelze"
# dependencies = []
# ///

import os
import sys
import subprocess

def main():
    if len(sys.argv) != 2:
        print("Usage: tomp3 <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.isfile(input_file):
        print("Error: File does not exist.")
        sys.exit(1)
    
    # Determine directory, base filename and remove extension.
    input_dir = os.path.dirname(input_file)
    input_basename = os.path.basename(input_file)
    input_name, _ = os.path.splitext(input_basename)
    
    # Build output file path.
    output_path = os.path.join(input_dir, input_name + ".mp3")
    
    # Run ffmpeg to convert the file to mp3.
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_file, "-acodec", "libmp3lame", "-ac", "1", "-ar", "16000", output_path],
            check=True
        )
    except subprocess.CalledProcessError:
        print("Error: Failed to convert file to mp3.")
        sys.exit(1)
    
    print("Converted successfully. Output file is at:", output_path)

if __name__ == "__main__":
    main()