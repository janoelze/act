#!/usr/bin/env python3
# /// script
# command = "transcript"
# description = "Fetch and display a YouTube video's transcript"
# aliases = ["yt-transcript", "yt-txt"]
# author = "Jan"
# dependencies = ["youtube-transcript-api"]
# ///

import sys
import re
import json
import argparse
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def extract_video_id(url_or_id: str) -> str:
    """Extract the 11‐character YouTube video ID from a URL or return it if it's already an ID."""
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        m = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_id)
        if not m:
            sys.exit("❌  Invalid YouTube URL or ID.")
        return m.group(1)
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", url_or_id):
        return url_or_id
    sys.exit("❌  Invalid YouTube URL or ID.")

def fetch_transcript(video_id: str, langs: list[str]) -> list[dict]:
    try:
        return YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
    except TranscriptsDisabled:
        sys.exit("❌  Transcripts are disabled for this video.")
    except NoTranscriptFound:
        sys.exit("❌  No transcript found for this video in the requested languages.")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display a YouTube video's transcript"
    )
    parser.add_argument(
        "video", help="YouTube video URL or 11‐char video ID"
    )
    parser.add_argument(
        "-l", "--language",
        default="en",
        help="Preferred transcript language code (e.g. en, de, es)."
    )
    parser.add_argument(
        "-t", "--translate",
        metavar="CODE",
        help="Translate transcript into this language code."
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output raw JSON instead of plain text."
    )
    args = parser.parse_args()

    vid = extract_video_id(args.video)
    languages = [args.translate] if args.translate else [args.language]
    transcript = fetch_transcript(vid, languages)

    if args.json:
        print(json.dumps(transcript, ensure_ascii=False, indent=2))
    else:
        for entry in transcript:
            start = entry.get("start", 0.0)
            text  = entry.get("text", "").strip()
            print(text)

if __name__ == "__main__":
    main()
