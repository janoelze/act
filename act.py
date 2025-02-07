import os
import sys
import ast
import subprocess
import urllib.request
import click
import time

# Directory where scripts are stored
SCRIPTS_DIR = os.path.join(os.path.expanduser("~"), ".act", "scripts")
QUARANTINE_DIR = os.path.join(os.path.expanduser("~"), ".act", "quarantine")
# Base URL for community scripts in the GitHub repository
REPO_URL_BASE = "https://raw.githubusercontent.com/janoelze/act/main/scripts"

def fetch_community_script(script_name):
    # """Fetch a script from the community repository."""
    # url = f"{REPO_URL_BASE}/{script_name}.py"
    # try:
    #     with urllib.request.urlopen(url) as response:
    #         return response.read().decode("utf-8")
    # except Exception as e:
    #     raise click.ClickException(f"Failed to download script: {e}")

    # for development purposes let's install the script from the local directory
    with open(f"{script_name}.py", "r") as f:
        return f.read()

def sanitize_script_name(script_name):
    """Enforce alphanumeric characters, dashes, and underscores only."""
    return "".join(c for c in script_name if c.isalnum() or c in "-_")

def ensure_scripts_dir():
    """Ensure the scripts directory exists."""
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(QUARANTINE_DIR, exist_ok=True)

def parse_header(file_content: str) -> dict:
    """
    Parse a header block in the given file content and return a dictionary of its key-value pairs.
    The header block is expected to be enclosed between lines starting with "# ///".
    
    For example, given a file with a header like:
    
        # /// script
        # command = "weather"
        # aliases = ["weather", "wttr", "wttr.in", "temperature", "temp"]
        # author = "janoelze"
        # dependencies = [
        #   "requests<3",
        # ]
        # ///
    
    This function will return:
    
        {
            "command": "weather",
            "aliases": ["weather", "wttr", "wttr.in", "temperature", "temp"],
            "author": "janoelze",
            "dependencies": ["requests<3"],
        }
    
    Note: Lines that do not follow a "key = value" assignment are ignored.
    """
    lines = file_content.splitlines()
    header_started = False
    header_lines = []

    for line in lines:
        stripped = line.strip()
        # Detect header delimiters: lines starting with "# ///"
        if stripped.startswith("# ///"):
            if not header_started:
                header_started = True
                continue  # skip the starting delimiter line
            else:
                # Stop at the ending delimiter
                break

        if header_started:
            # Only consider lines that are commented out (start with '#')
            if stripped.startswith("#"):
                # Remove the leading '#' and any extra whitespace
                content = stripped[1:].strip()
                header_lines.append(content)

    # Combine header lines into a single string. This will correctly handle
    # multi-line assignments (like lists spanning several lines).
    header_str = "\n".join(header_lines)

    # Parse the header string as Python code using the ast module.
    try:
        tree = ast.parse(header_str, mode='exec')
    except SyntaxError as e:
        raise ValueError("Failed to parse header content") from e

    header_dict = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            # Ensure it's a simple assignment to a single variable name
            if len(node.targets) != 1:
                continue
            target = node.targets[0]
            if isinstance(target, ast.Name):
                key = target.id
                try:
                    # Use literal_eval to safely evaluate the value expression
                    value = ast.literal_eval(node.value)
                except Exception as e:
                    raise ValueError(f"Unable to evaluate value for key '{key}'") from e
                header_dict[key] = value

    return header_dict

def parse_script_metadata(file_path):
    """
    Parse the inline dependency header of a script file.
    Returns a dict with keys like 'command', 'aliases', 'author', 'dependencies'.
    """
    metadata = {}
    with open(file_path, "r", encoding="utf-8") as f:
        metadata = parse_header(f.read())
    return metadata

def find_script(script_identifier):
    """
    Find a script file by matching the given identifier to the script's 'command'
    or one of its 'aliases' in the metadata.
    Returns the full path of the script or None if not found.
    """
    ensure_scripts_dir()
    for entry in os.listdir(SCRIPTS_DIR):
        if entry.endswith(".py"):
            script_path = os.path.join(SCRIPTS_DIR, entry)
            metadata = parse_script_metadata(script_path)
            # Check if the identifier matches the 'command'
            if metadata.get("command") == script_identifier:
                return script_path
            # Check if the identifier is among the aliases
            aliases = metadata.get("aliases", [])
            if isinstance(aliases, list) and script_identifier in aliases:
                return script_path
    return None

@click.group()
def cli():
    """act - A CLI tool to manage and run python scripts."""
    ensure_scripts_dir()

@cli.command()
@click.argument("script_name", required=False)
def create(script_name):
    """
    Create a new script.
    
    If SCRIPT_NAME is not provided, you will be prompted for one.
    A new script with a template header is created and then opened in your default editor.
    """
    if not script_name:
        script_name = click.prompt("Enter script command name", type=str)
    filename = f"{script_name}.py"
    script_path = os.path.join(SCRIPTS_DIR, filename)
    if os.path.exists(script_path):
        raise click.ClickException(f"Script '{script_name}' already exists.")
    # Template header with metadata
    template = f'''# /// script
# command = "{script_name}"
# aliases = ["{script_name}"]
# author = "your_name_here"
# dependencies = []
# ///

# Write your code below
'''
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(template)
    click.echo(f"Script '{script_name}' created at {script_path}")
    # Open the newly created script in the editor
    ctx = click.get_current_context()
    ctx.invoke(edit, script_identifier=script_name)

@cli.command()
@click.argument("script_identifier")
def edit(script_identifier):
    """
    Edit an existing script in your default editor.
    
    SCRIPT_IDENTIFIER can be the command name or one of its aliases.
    """
    script_path = find_script(script_identifier)
    if not script_path:
        raise click.ClickException(f"Script '{script_identifier}' not found.")
    editor = os.environ.get("EDITOR", "nano")
    subprocess.run([editor, script_path])

@cli.command()
@click.argument("script_identifier")
@click.argument("args", nargs=-1)
def run(script_identifier, args):
  """
  Run a script.
  
  SCRIPT_IDENTIFIER is the command name or one of its aliases.
  Any additional arguments will be passed to the script.
  Before running, the script's dependencies (if any) are installed via pip.
  """
  script_path = find_script(script_identifier)
  if not script_path:
    raise click.ClickException(f"Script '{script_identifier}' not found.")
  click.echo(f"Running script '{script_identifier}'...\n")
  start_time = time.time()
  # Run the script with any additional arguments
  result = subprocess.run(['uv', 'run', '--quiet', script_path] + list(args))
  end_time = time.time()
  elapsed = end_time - start_time
  if result.returncode == 0:
    click.secho(f"Done in {elapsed:.2f}s.", fg="green")
  else:
    click.secho(f"Failed with exit code {result.returncode}.", fg="red")
  sys.exit(result.returncode)

@cli.command()
@click.argument("script_identifier")
def delete(script_identifier):
    """
    Delete a script.
    
    SCRIPT_IDENTIFIER is the command name or one of its aliases.
    """
    script_path = find_script(script_identifier)
    if not script_path:
        raise click.ClickException(f"Script '{script_identifier}' not found.")
    os.remove(script_path)
    click.echo(f"Script '{script_identifier}' deleted.")

@cli.command(name="list")
def list_scripts():
    """
    List all available scripts.
    
    The command names (as specified in the script header) are printed.
    """
    ensure_scripts_dir()
    found = False
    for entry in os.listdir(SCRIPTS_DIR):
        if entry.endswith(".py"):
            script_path = os.path.join(SCRIPTS_DIR, entry)
            metadata = parse_script_metadata(script_path)
            command = metadata.get("command", entry)
            click.echo(command)
            found = True
    if not found:
        click.echo("No scripts found.")

@cli.command(name="meta")
@click.argument("script_identifier")
def meta(script_identifier):
    """Display the metadata of a script."""
    script_path = find_script(script_identifier)
    if not script_path:
        raise click.ClickException(f"Script '{script_identifier}' not found.")
    metadata = parse_script_metadata(script_path)
    for key, value in metadata.items():
        click.echo(f"{key}: {value}")


@cli.command()
@click.argument("script_name")
def install(script_name):
  """
  Install a script from the community repository.
  
  The script is downloaded from the GitHub repository and stored locally.
  """
  clean_script_name = sanitize_script_name(script_name)
  content = fetch_community_script(clean_script_name)

  if not content:
    raise click.ClickException(f"Failed to download script: {e}")
  
  script_path = os.path.join(QUARANTINE_DIR, f"{clean_script_name}.py")

  with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)

  metadata = parse_script_metadata(script_path)

  # ensure the script has the required fields
  for field in ["command", "author"]:
    if field not in metadata:
      raise click.ClickException(f"Script is missing required field '{field}'")

  # click.echo(f"Installing script '{script_name}' from {REPO_URL_BASE}/{script_name}.py")
  # # Ask for confirmation
  prompt = (
    f"'{clean_script_name}' is a community script by {metadata['author']}.\r\n"
    "It may access the internet, read and write files, and use third party libraries.\r\n"
    "Are you sure you want to install this script?"
  )
  
  if not click.confirm(prompt):
    click.secho("Installation aborted.", fg="red")
    return
  try:
    content = fetch_community_script(script_name)
  except Exception as e:
    raise click.ClickException(f"Failed to download script: {e}")
  
  # move the script from quarantine to the scripts directory
  new_script_path = os.path.join(SCRIPTS_DIR, f"{clean_script_name}.py")
  os.rename(script_path, new_script_path)

  click.secho(f"Script '{clean_script_name}' installed successfully.", fg="green")

if __name__ == "__main__":
    cli()
