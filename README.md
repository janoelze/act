# ACT

`act` is a command-line tool to manage custom Python scripts.

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

## SCRIPTS

<!-- ACT_SCRIPTS_START -->
| Title | Description |  |
| --- | --- | --- |
| **diskclean** | List the largest files and directories in your home directory to help free up disk space (optimized with concurrency) (Created by janoelze) | [View](./community-scripts/diskclean.py) |
| **tomp3** | Convert any file format to an MP3 using ffmpeg (Created by janoelze) | [View](./community-scripts/tomp3.py) |
| **benchmark** | Benchmark a given URL using ApacheBench (Created by janoelze) | [View](./community-scripts/benchmark.py) |
| **webmp4** | Convert any video format to a web-ready MP4 with small file size and reasonable resolution (Created by janoelze) | [View](./community-scripts/webmp4.py) |
| **ytdl** | Download YouTube videos via yt-dlp (Created by janoelze) | [View](./community-scripts/ytdl.py) |
| **weather** | Get the current weather in Berlin (Created by janoelze) | [View](./community-scripts/weather.py) |
| **resize** | Resizes the images in the current directory to a specified width (Created by janoelze) | [View](./community-scripts/resize.py) |
| **ytdl-audio** | Download the audio of a YouTube video via yt-dlp (Created by janoelze) | [View](./community-scripts/ytdl-audio.py) |
| **vpntoggle** | Toggle VPN connection using OpenVPN (Created by janoelze) | [View](./community-scripts/vpntoggle.py) |
<!-- ACT_SCRIPTS_END -->

## COMMANDS

- **create [script_name]**  
  Create a new script with a template header for metadata.  
  Example: `act create weather`

- **edit <script_identifier>**  
  Open an existing script in your default editor.  
  Example: `act edit weather`

- **run <script_identifier> [args]**  
  Execute a script, automatically handling its dependencies.  
  Example: `act run weather --city Boston`

- **delete <script_identifier>**  
  Remove an existing script.  
  Example: `act delete weather`

- **list**  
  List all available scripts by their command names.  
  Example: `act list`

- **meta <script_identifier>**  
  Display metadata of a specific script.  
  Example: `act meta weather`

- **install <script_name>**  
  Install a community script from the GitHub repository.  
  Example: `act install weather`