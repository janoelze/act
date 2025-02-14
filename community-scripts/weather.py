# /// script
# command = "weather"
# description = "Get the current weather in Berlin"
# aliases = ["weather", "wttr", "wttr.in", "temperature", "temp"]
# author = "janoelze"
# dependencies = [
#   "requests<3",
# ]
# ///

import requests
import argparse

parser = argparse.ArgumentParser(description="Get the current weather for a specified city")
parser.add_argument("--city", type=str, required=True, help="Name of the city")
args = parser.parse_args()

# use wttr.in to get the weather for the specified city
resp = requests.get(f"https://wttr.in/{args.city}?format=3")
print(resp.text.strip())