## act spec

`act` is a command line tool that allows you to run python scripts.

- scripts are kept in ~/.act/scripts
- scripts use UV's new inline dependency headers to define required third party libraries
- a cli interfact allows users to create, edit, run, and delete scripts
- scripts can be merged into the upstream repository to make them available to the community

### an example script

```python
# /// script
# command = "weather"
# aliases = ["weather", "wttr", "wttr.in", "temperature", "temp"]
# author = "janoelze"
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests

# use wttr.in to get the weather in Berlin
resp = requests.get("https://wttr.in/Berlin?format=3")
print(resp.text)
```

### another example script

```python
# /// script
# command = "resize-images"
# aliases = ["resize", "resizeimage", "thumbnail"]
# author = "janoelze"
# dependencies = [
#   "Pillow",
# ]
# ///

from PIL import Image
import sys

print(sys.argv)

# resize an image
img = Image.open("input.jpg")
img.thumbnail((128, 128))
img.save("output.jpg")
```

### the act script format

- the script format is a python file with a header that contains metadata
- the header is a comment block that starts with `# /// script` and ends with `# ///`
- the header contains metadata in the form of key-value pairs
- the metadata is used by the act cli to identify the script
- the metadata is used by the act cli to install dependencies
- the metadata is used by the act cli to list available scripts

### the cli

- `act create` - create a new script
- `act edit $1` - opens the script in the default editor
- `act run $1` - identifies the script by title or command and runs it
- `act delete $1` - deletes the script
- `act list` - lists all available scripts
- `act install $1` - installs a script from the github repository

### the repository

the github repository contains the source code for act and a folder called `scripts` that contains all the scripts that are available to the community. the repository is managed by the act maintainers and scripts can be submitted via pull request. the repository is located at https://github.com/janoelze/act.

### Using act

- act is installed via pip or uv
- act creates a folder in the user's home directory called `~/.act`
- act creates a folder in the user's home directory called `~/.act/scripts`
- act uses the inline dependency headers to install required libraries
- act exposes available scripts via tab completion

### act internals

- act uses the `subprocess` module to run scripts
- act hands down the arguments given to the `run` command to the script
- uv is a python package and project manager that manages environments and dependencies
- uv automatically picks up on dependencies in the script header and installs them

### act interface

```zsh
$ act run weather
> 5°C 🌧 
> Done in 0.05s
```

```zsh
$ act install resize-images
> Installing script resize-images
> 'resize-images' is a community script by 'janoelze' and will be able to access the internet, read and write files, and use third party libraries. Are you sure you want to install this script? [y/n] y
> Installed 'resize-images' in 0.05s
```

```zsh
$ act list
> weather
> resize-images
```
