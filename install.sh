#!/usr/bin/env bash
set -e

# Check for required commands
command -v uv >/dev/null 2>&1 || { echo >&2 "uv is required but not installed. Aborting."; exit 1; }
command -v git >/dev/null 2>&1 || { echo >&2 "git is required but not installed. Aborting."; exit 1; }
command -v curl >/dev/null 2>&1 || { echo >&2 "curl is required but not installed. Aborting."; exit 1; }

# Set up directories and repository URL
ACT_DIR="$HOME/.act"
ACT_BIN_DIR="$ACT_DIR/bin"
REPO_URL="https://github.com/janoelze/act.git"
ACT_SCRIPT="$ACT_DIR/act.py"

echo "Installing act..."

# If the act directory exists and is a git repository, update it.
if [ -d "$ACT_DIR" ]; then
    if [ -d "$ACT_DIR/.git" ]; then
        echo "Found existing act installation. Updating..."
        cd "$ACT_DIR"
        git pull --ff-only
    else
        echo "Directory $ACT_DIR already exists and does not seem to be a git repository."
        echo "Assuming act is already installed. If you experience issues, please remove or move $ACT_DIR and re-run this installer."
    fi
else
    echo "Cloning act repository into $ACT_DIR..."
    git clone "$REPO_URL" "$ACT_DIR"
fi

# Create the bin directory if it doesn't exist
mkdir -p "$ACT_BIN_DIR"

# Create a wrapper script to run act
ACT_WRAPPER="$ACT_BIN_DIR/act"
cat > "$ACT_WRAPPER" << 'EOF'
#!/usr/bin/env bash
uv run --quiet "$HOME/.act/act.py" "$@"
EOF

chmod +x "$ACT_WRAPPER"

# Run the 'link' command to create command shims for installed scripts
uv run --quiet "$ACT_SCRIPT" link

# Prompt to add PATH if not already present in shell config.
if [[ "$SHELL" == *"zsh" ]]; then
    CONFIG_FILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash" ]]; then
    CONFIG_FILE="$HOME/.bashrc"
else
    CONFIG_FILE="$HOME/.bashrc"
fi

# todo: check the actual $PATH variable, not just the file contents
if ! grep -q 'export PATH="\$HOME/.act/bin:\$PATH"' "$CONFIG_FILE" 2>/dev/null; then
    read -p "Do you want to add '$ACT_BIN_DIR' to your PATH in $CONFIG_FILE? (y/n): " add_path
    if [[ "$add_path" == "y" || "$add_path" == "Y" ]]; then
        echo 'export PATH="$HOME/.act/bin:$PATH"' >> "$CONFIG_FILE"
        echo "Added PATH extension to $CONFIG_FILE."
    fi
fi

echo ""
echo "act has been installed into $ACT_DIR."