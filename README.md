# act — A CLI Tool for Managing Python Scripts

## NAME
act — A command-line tool to create, edit, run, install, and manage Python scripts.

## SYNOPSIS
    act <command> [options] [arguments]

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

## INSTALLATION
1. Clone or download the repository.
2. Ensure Python and required dependencies are installed.
3. Place your scripts in the designated directory automatically set up by act.

## AUTHOR
janoelze

## COPYRIGHT
MIT License

## SEE ALSO
Python, Click, subprocess

// ...existing content...
