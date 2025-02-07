import os
import sys
import ast
import subprocess
import urllib.request
import click
import time

# Base directory for act
BASE_ACT_DIR = os.path.join(os.path.expanduser("~"), ".act")
# Directory for local (user-created) scripts
LOCAL_SCRIPTS_DIR = os.path.join(BASE_ACT_DIR, "local")
# Directory for community scripts
COMMUNITY_SCRIPTS_DIR = os.path.join(BASE_ACT_DIR, "community")
# Directory for quarantine (used during installation)
QUARANTINE_DIR = os.path.join(BASE_ACT_DIR, "quarantine")
# Base URL for community scripts in the GitHub repository
REPO_URL_BASE = "https://raw.githubusercontent.com/janoelze/act/main/community-scripts"

def fetch_community_script(script_name):
    # """Fetch a script from the community repository."""
    # url = f"{REPO_URL_BASE}/{script_name}.py"
    # try:
    #     with urllib.request.urlopen(url) as response:
    #         return response.read().decode("utf-8")
    # except Exception as e:
    #     raise click.ClickException(f"Failed to download script: {e}")

    # For development purposes let's install the script from the local directory
    with open(f"{script_name}.py", "r") as f:
        return f.read()

def sanitize_script_name(script_name):
    """Enforce alphanumeric characters, dashes, and underscores only."""
    return "".join(c for c in script_name if c.isalnum() or c in "-_")

def ensure_scripts_dir():
    """Ensure that all required directories exist."""
    os.makedirs(LOCAL_SCRIPTS_DIR, exist_ok=True)
    os.makedirs(COMMUNITY_SCRIPTS_DIR, exist_ok=True)
    os.makedirs(QUARANTINE_DIR, exist_ok=True)

def parse_header(file_content: str) -> dict:
    """
    Parse a header block in the given file content and return a dictionary of its key-value pairs.
    The header block is expected to be enclosed between lines starting with "# ///".
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
            if stripped.startswith("#"):
                # Remove the leading '#' and extra whitespace
                content = stripped[1:].strip()
                header_lines.append(content)

    header_str = "\n".join(header_lines)

    try:
        tree = ast.parse(header_str, mode='exec')
    except SyntaxError as e:
        raise ValueError("Failed to parse header content") from e

    header_dict = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if len(node.targets) != 1:
                continue
            target = node.targets[0]
            if isinstance(target, ast.Name):
                key = target.id
                try:
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
    with open(file_path, "r", encoding="utf-8") as f:
        return parse_header(f.read())

def find_script(script_identifier):
    """
    Find a script by its identifier.
    
    If the identifier is prefixed with a namespace (e.g. "community:weather" or "local:weather"),
    the search is limited to that namespace. Without a prefix, the search first looks in local scripts,
    then in community scripts.
    
    Returns the full path of the script or None if not found.
    """
    ensure_scripts_dir()
    namespace = None
    command = script_identifier

    if ":" in script_identifier:
        namespace, command = script_identifier.split(":", 1)
        namespace = namespace.lower()

    if namespace == "local":
        directories = [LOCAL_SCRIPTS_DIR]
    elif namespace == "community":
        directories = [COMMUNITY_SCRIPTS_DIR]
    else:
        directories = [LOCAL_SCRIPTS_DIR, COMMUNITY_SCRIPTS_DIR]

    for directory in directories:
        for entry in os.listdir(directory):
            if entry.endswith(".py"):
                script_path = os.path.join(directory, entry)
                try:
                    metadata = parse_script_metadata(script_path)
                except Exception:
                    continue
                if metadata.get("command") == command:
                    return script_path
                aliases = metadata.get("aliases", [])
                if isinstance(aliases, list) and command in aliases:
                    return script_path
    return None

@click.group()
def cli():
    """act - A CLI tool to manage and run Python scripts."""
    ensure_scripts_dir()

@cli.command()
@click.argument("script_name", required=False)
def create(script_name):
    """
    Create a new script.
    
    If SCRIPT_NAME is not provided, you will be prompted for one.
    A new script with a template header is created and then opened in your default editor.
    (Local scripts are stored in the 'local' namespace.)
    """
    if not script_name:
        script_name = click.prompt("Enter script command name", type=str)
    filename = f"{script_name}.py"
    script_path = os.path.join(LOCAL_SCRIPTS_DIR, filename)
    if os.path.exists(script_path):
        raise click.ClickException(f"Local script '{script_name}' already exists.")
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
    click.echo(f"Local script '{script_name}' created at {script_path}")
    ctx = click.get_current_context()
    ctx.invoke(edit, script_identifier=script_name)

@cli.command()
@click.argument("script_identifier")
def edit(script_identifier):
    """
    Edit an existing script in your default editor.
    
    SCRIPT_IDENTIFIER can be the command name or one of its aliases.
    You can also prefix with a namespace (e.g. "community:weather").
    """
    script_path = find_script(script_identifier)
    if not script_path:
        raise click.ClickException(f"Script '{script_identifier}' not found.")
    editor = os.environ.get("EDITOR", "nano")
    subprocess.run([editor, script_path])

@cli.command()
@click.option("-q", "--quiet", is_flag=True, help="Suppress completion message.")
@click.argument("script_identifier", required=False)
@click.argument("args", nargs=-1)
def run(quiet, script_identifier, args):
    """
    Run a script.
    
    SCRIPT_IDENTIFIER is the command name (optionally namespaced) or one of its aliases.
    If not supplied, a list of installed scripts is displayed for selection.
    Additional arguments will be passed to the script.
    
    The search first checks local scripts, then community scripts.
    """
    if not script_identifier:
        ensure_scripts_dir()
        scripts = []
        # Collect local scripts
        for entry in os.listdir(LOCAL_SCRIPTS_DIR):
            if entry.endswith(".py"):
                script_path = os.path.join(LOCAL_SCRIPTS_DIR, entry)
                metadata = parse_script_metadata(script_path)
                command = metadata.get("command", entry)
                scripts.append(("local:" + command, script_path))
        # Collect community scripts
        for entry in os.listdir(COMMUNITY_SCRIPTS_DIR):
            if entry.endswith(".py"):
                script_path = os.path.join(COMMUNITY_SCRIPTS_DIR, entry)
                metadata = parse_script_metadata(script_path)
                command = metadata.get("command", entry)
                scripts.append(("community:" + command, script_path))
        if not scripts:
            raise click.ClickException("No installed scripts found.")
        click.echo("Installed scripts:")
        for idx, (command, _) in enumerate(scripts, start=1):
            click.echo(f"{idx}: {command}")
        choice = click.prompt("Enter the number of the script to run", type=int)
        if choice < 1 or choice > len(scripts):
            raise click.ClickException("Invalid selection.")
        script_identifier, script_path = scripts[choice - 1]
    else:
        script_path = find_script(script_identifier)
        if not script_path:
            raise click.ClickException(f"Script '{script_identifier}' not found.")
    start_time = time.time()
    # Run the script with any additional arguments (using 'uv run' as in the original code)
    result = subprocess.run(['uv', 'run', '--quiet', script_path] + list(args))
    elapsed = time.time() - start_time
    if result.returncode == 0 and not quiet:
        click.secho(f"Done in {elapsed:.2f}s.", fg="green")
    elif result.returncode != 0:
        click.secho(f"Failed with exit code {result.returncode}.", fg="red")
    sys.exit(result.returncode)

@cli.command()
@click.argument("script_identifier")
def delete(script_identifier):
    """
    Delete a script.
    
    SCRIPT_IDENTIFIER is the command name (optionally namespaced) or one of its aliases.
    """
    script_path = find_script(script_identifier)
    if not script_path:
        raise click.ClickException(f"Script '{script_identifier}' not found.")
    os.remove(script_path)
    click.echo(f"Script '{script_identifier}' deleted.")

@cli.command(name="list")
def list_scripts():
    """
    List all available scripts, grouped by namespace.
    """
    ensure_scripts_dir()
    found = False
    click.echo("Local scripts:")
    for entry in os.listdir(LOCAL_SCRIPTS_DIR):
        if entry.endswith(".py"):
            script_path = os.path.join(LOCAL_SCRIPTS_DIR, entry)
            metadata = parse_script_metadata(script_path)
            command = metadata.get("command", entry)
            click.echo(f"  {command}")
            found = True
    click.echo("Community scripts:")
    for entry in os.listdir(COMMUNITY_SCRIPTS_DIR):
        if entry.endswith(".py"):
            script_path = os.path.join(COMMUNITY_SCRIPTS_DIR, entry)
            metadata = parse_script_metadata(script_path)
            command = metadata.get("command", entry)
            click.echo(f"  {command}")
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
    
    The script is downloaded from the GitHub repository, stored in quarantine, and then,
    after confirmation, moved to the community scripts directory.
    """
    clean_script_name = sanitize_script_name(script_name)
    content = fetch_community_script(clean_script_name)

    if not content:
        raise click.ClickException("Failed to download script.")

    quarantine_path = os.path.join(QUARANTINE_DIR, f"{clean_script_name}.py")
    with open(quarantine_path, "w", encoding="utf-8") as f:
        f.write(content)

    metadata = parse_script_metadata(quarantine_path)

    for field in ["command", "author"]:
        if field not in metadata:
            raise click.ClickException(f"Script is missing required field '{field}'")

    prompt = (
        f"'{clean_script_name}' is a community script by {metadata['author']}.\n"
        "It may access the internet, read and write files, and use third party libraries.\n"
        "Are you sure you want to install this script?"
    )
    
    if not click.confirm(prompt):
        click.secho("Installation aborted.", fg="red")
        return

    # Check for name collisions in the community namespace
    new_script_path = os.path.join(COMMUNITY_SCRIPTS_DIR, f"{clean_script_name}.py")
    if os.path.exists(new_script_path):
        raise click.ClickException(f"A community script with command '{clean_script_name}' is already installed.")

    # Move the script from quarantine to the community directory
    os.rename(quarantine_path, new_script_path)
    click.secho(f"Community script '{clean_script_name}' installed successfully.", fg="green")

if __name__ == "__main__":
    cli()