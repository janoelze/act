# /// script
# command = "ytdl-audio"
# description = "Download the audio of a YouTube video via yt-dlp"
# aliases = ["youtubemp3", "yt-mp3", "ytdl-mp3", "yt-dl-mp3", "yt-dlp-mp3", "yt2mp3", "youtube2mp3"]
# author = "janoelze"
# dependencies = [
#   "yt_dlp",
# ]
# ///

import sys
from yt_dlp import YoutubeDL

def download_video(url):
    # You can customize options here; for now, we'll download the best quality audio available.
    ydl_opts = {
        'format': 'bestaudio',  # download the best quality audio available
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
