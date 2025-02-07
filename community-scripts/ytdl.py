# /// script
# command = "ytdl"
# description = "Download YouTube videos via yt-dlp"
# aliases = ["youtube", "yt", "ytdl", "yt-dl", "yt-dlp"]
# author = "janoelze"
# dependencies = [
#   "yt_dlp",
# ]
# ///

import sys
from yt_dlp import YoutubeDL

def download_video(url):
    # You can customize options here; for now, we'll download the best quality available.
    ydl_opts = {
        'format': 'best',  # download the best quality available
        # Uncomment the following line to set an output template (e.g., filename as video title)
        # 'outtmpl': '%(title)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    if len(sys.argv) != 2:
        print("Please provide a YouTube URL to download.")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    download_video(youtube_url)

if __name__ == "__main__":
    main()
