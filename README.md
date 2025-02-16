# ACT

`act` allows you to install, run, and manage scripts with ease.

## WHY

I really love the simplicity of uv's [inline dependency definitions](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies) right on top of Python files. `act` takes this idea and extends the script header with a `command` property and then allows global calls to these scripts by their command name via, for example, `act run helloworld`. Additionally shims are created for each script in the `~/.act/bin` directory, making script execution easy to remember.

## SYNOPSIS

    act <command> [options] [arguments]

## USAGE

Installs a script from the [community-scripts](https://github.com/janoelze/act/tree/main/community-scripts) directory:


```shell
$ act install weather
'weather' is a community script by janoelze.
It may access the internet, read and write files, and use third party libraries.
Are you sure you want to install this script? [y/N]: y
Community script 'weather' installed successfully.
Successfully recreated shims for 2 scripts in '/Users/janoelze/.act/bin'.
```

Runs the script with the city argument:

```shell
# Runs the weather script with the city argument
$ act run weather --city Berlin
Berlin: 🌨  +2°C
Done in 0.50s.
```

Or—if you've added the ~/.act/bin directory to your PATH—you can run the script directly:

```shell
# Runs the weather script with the city argument
$ weather --city Berlin
Berlin: 🌨  +2°
Done in 0.50s.
```

## INSTALLATION

You can install or update act by running the following command in your terminal:

```shell
curl -fsSL https://raw.githubusercontent.com/janoelze/act/main/install.sh | sh
```

Uninstall act by running the following command:

```shell
curl -fsSL https://raw.githubusercontent.com/janoelze/act/main/uninstall.sh | sh
```

## COMMUNITY SCRIPTS

<!-- ACT_SCRIPTS_START -->
| Command | Description |  |
| --- | --- | --- |
| **benchmark** | Benchmark a given URL using ApacheBench (Created by janoelze) | [View](./community-scripts/benchmark.py) |
| **diskclean** | List the largest files and directories in your home directory to help free up disk space (optimized with concurrency) (Created by janoelze) | [View](./community-scripts/diskclean.py) |
| **helloworld** | A simple script that prints 'Hello, world!' (Created by janoelze) | [View](./community-scripts/helloworld.py) |
| **resize** | Resizes the images in the current directory to a specified width (Created by janoelze) | [View](./community-scripts/resize.py) |
| **tomp3** | Convert any file format to an MP3 using ffmpeg (Created by janoelze) | [View](./community-scripts/tomp3.py) |
| **tomp4** | Convert any video format to a web-ready MP4 with small file size and reasonable resolution (Created by janoelze) | [View](./community-scripts/tomp4.py) |
| **vpntoggle** | Toggle VPN connection using OpenVPN (Created by janoelze) | [View](./community-scripts/vpntoggle.py) |
| **weather** | Get the current weather in Berlin (Created by janoelze) | [View](./community-scripts/weather.py) |
| **ytdl** | Download YouTube videos via yt-dlp (Created by janoelze) | [View](./community-scripts/ytdl.py) |
| **ytdl-audio** | Download the audio of a YouTube video via yt-dlp (Created by janoelze) | [View](./community-scripts/ytdl-audio.py) |
<!-- ACT_SCRIPTS_END -->

## SCRIPT ANATOMY

The script header contains metadata that describes the script's behavior and dependencies.

```python
#!/usr/bin/env python3
# /// script
# command = "helloworld"
# description = "Hello, world!"
# aliases = ["hw"]
# author = "janoelze"
# dependencies = []
# ///

import os

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```

Aliases are alternative names for the script that can be used to run it. For example, the `helloworld` script can also be run with the `hw` command:

```shell
$ act run helloworld
Hello, world!
$ act run hw
Hello, world!
$ hw
Hello, world!
```

## COMMANDS

- **create [script_name]**  
  Create a new script with a template header for metadata.<br>
  Example: `act create weather`

- **edit <script_name>**  
  Open an existing script in your default editor.<br>
  Example: `act edit weather`

- **run <script_name> [args]**  
  Execute a script, automatically handling its dependencies.<br>
  Example: `act run weather --city Boston`

- **delete <script_name>**  
  Remove an existing script.<br>
  Example: `act delete weather`

- **list**  
  List all available scripts by their command names.<br>
  Example: `act list`

- **meta <script_name>**  
  Display metadata of a specific script.<br>
  Example: `act meta weather`

- **install <script_name>**  
  Install a community script from the GitHub repository.<br>
  Example: `act install weather`

- **link**  
  Create shims for all installed scripts, making them globally accessible.<br>
  Example: `act link`