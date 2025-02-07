#!/usr/bin/env python3
# /// script
# command = "diskclean"
# description = "List the largest files and directories in your home directory to help free up disk space (pure Python)"
# aliases = ["diskclean", "diskusage", "du", "clean-disk"]
# author = "janoelze"
# dependencies = []
# ///

import os
import sys

def human_readable_size(size, decimal_places=1):
    """Convert a size in bytes into a human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.{decimal_places}f}{unit}"
        size /= 1024
    return f"{size:.{decimal_places}f}PB"

def main():
    home_dir = os.path.expanduser("~")
    files_list = []      # List of tuples: (path, size, "file")
    dirs_sizes = {}      # Dictionary mapping directory path -> cumulative size

    # Walk the home directory from the bottom up
    for root, dirs, files in os.walk(home_dir, topdown=False, onerror=lambda e: None):
        total = 0
        # Process files in the current directory.
        for f in files:
            file_path = os.path.join(root, f)
            try:
                size = os.path.getsize(file_path)
                files_list.append((file_path, size, "file"))
                total += size
            except Exception:
                # Ignore files that can't be accessed
                continue

        # Add sizes of subdirectories (which have been processed already)
        for d in dirs:
            dpath = os.path.join(root, d)
            # If we computed a size for this subdirectory, add it.
            if dpath in dirs_sizes:
                total += dirs_sizes[dpath]

        # Save the total cumulative size for this directory.
        dirs_sizes[root] = total

    # Build a list of directory entries.
    dirs_list = [(path, size, "dir") for path, size in dirs_sizes.items()]

    # Combine files and directories.
    all_items = files_list + dirs_list

    # Sort items by size descending.
    all_items_sorted = sorted(all_items, key=lambda x: x[1], reverse=True)

    # Print the top 20 largest items.
    print(f"{'Size':>10} {'Type':>4}  Path")
    print("-" * 80)
    for item in all_items_sorted[:20]:
        path, size, typ = item
        print(f"{human_readable_size(size):>10} {typ:>4}  {path}")

if __name__ == "__main__":
    main()
