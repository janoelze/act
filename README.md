# act

`act` is a command-line tool to manage custom Python scripts.

## SYNOPSIS

    act <command> [options] [arguments]

## EXAMPLES

Installs a script from the /community-scripts directory:


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

## DESCRIPTION

act helps you manage your custom Python scripts by providing commands to create, edit, run, install community scripts, and view metadata. It organizes scripts in a dedicated directory and lets you manage dependencies automatically.

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