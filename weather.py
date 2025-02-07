# /// script
# command = "weather"
# aliases = ["weather", "wttr", "wttr.in", "temperature", "temp"]
# author = "janoelze"
# dependencies = [
#   "requests<3",
# ]
# ///

import requests

# use wttr.in to get the weather in Berlin
resp = requests.get("https://wttr.in/Berlin?format=3")
print(resp.text.strip())