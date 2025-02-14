#!/usr/bin/env bash
set -e

ACT_DIR="$HOME/.act"

if [ ! -d "$ACT_DIR" ]; then
    echo "act is not installed in $ACT_DIR. Nothing to uninstall."
    exit 0
fi

echo "WARNING: This will permanently remove the act installation located at:"
echo "         $ACT_DIR"
echo "         This includes all installed scripts, configurations, and bin shims."
echo ""
read -p "Are you sure you want to proceed? (y/N): " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo "Uninstalling act..."
    rm -rf "$ACT_DIR"
    echo "act has been uninstalled."
    echo ""
    echo "Reminder: If you added '$HOME/.act/bin' to your PATH, please remove it from your shell configuration."
else
    echo "Uninstallation aborted."
fi