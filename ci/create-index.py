import os
import json
import re


def extract_header_info(file_path):
    """Extract command, description, author, and aliases from the header."""
    header_info = {
        "command": None,
        "description": None,
        "author": None,
        "aliases": []
    }

    with open(file_path, 'r') as f:
        for line in f:
            if match := re.match(r'#\s*command\s*=\s*"(.*?)"', line):
                header_info['command'] = match.group(1)
            elif match := re.match(r'#\s*description\s*=\s*"(.*?)"', line):
                header_info['description'] = match.group(1)
            elif match := re.match(r'#\s*author\s*=\s*"(.*?)"', line):
                header_info['author'] = match.group(1)
            elif match := re.match(r'#\s*aliases\s*=\s*(\[.*\])', line):
                header_info['aliases'] = json.loads(match.group(1))

    return header_info


def create_index(directory):
    """Create an index of scripts with metadata from the headers."""
    index = {"scripts": []}

    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            header_info = extract_header_info(file_path)

            if header_info['command']:
                index['scripts'].append({
                    "file": file_path,
                    "command": header_info['command'],
                    "description": header_info['description'],
                    "author": header_info['author'],
                    "aliases": header_info['aliases']
                })

    # Write the index to a file
    index_path = os.path.join(directory, 'index')
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=4)

    print(f"Index created at {index_path}")

    # Update the README file
    self_dir = os.path.dirname(os.path.realpath(__file__))
    # print(f"Self dir: {}")
    readme_path = os.path.join(self_dir, '..', 'README.md')

    print(f"Updating README at {readme_path}")

    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            content = f.read()

        table_header = "| Title | Description |  |\n| --- | --- | --- |\n"
        table_rows = "\n".join(
            f"| **{script['command']}** | {script['description'] or ''} | [View Script]({script['file']}) |"
            for script in index['scripts']
        )
        scripts_list = table_header + table_rows

        updated_content = re.sub(
            r'<!-- ACT_SCRIPTS_START -->.*<!-- ACT_SCRIPTS_END -->',
            f'<!-- ACT_SCRIPTS_START -->\n{scripts_list}\n<!-- ACT_SCRIPTS_END -->',
            content,
            flags=re.DOTALL
        )

        with open(readme_path, 'w') as f:
            f.write(updated_content)

        print(f"Updated README at {readme_path}")


if __name__ == "__main__":
    community_scripts_dir = "./community-scripts"
    create_index(community_scripts_dir)