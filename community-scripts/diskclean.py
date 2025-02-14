#!/usr/bin/env python3
# /// script
# command = "diskclean"
# description = "List the largest files and directories in your home directory to help free up disk space (optimized with concurrency)"
# aliases = ["diskclean", "diskusage", "du", "clean-disk"]
# author = "janoelze"
# dependencies = []
# ///

import os
import sys
import concurrent.futures

def human_readable_size(size, decimal_places=1):
    """Convert a size in bytes into a human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.{decimal_places}f}{unit}"
        size /= 1024
    return f"{size:.{decimal_places}f}PB"

def scan_directory(path, executor):
    """
    Recursively scan a directory and return a tuple:
      (total_size, list_of_items)
    where list_of_items is a list of tuples (path, size, type)
    with type being "file" or "dir".
    """
    total = 0
    items = []
    futures = []
    
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    # Skip symbolic links to avoid recursion loops
                    if entry.is_symlink():
                        continue

                    if entry.is_file(follow_symlinks=False):
                        size = entry.stat(follow_symlinks=False).st_size
                        total += size
                        items.append((entry.path, size, "file"))
                    elif entry.is_dir(follow_symlinks=False):
                        # Schedule a recursive scan for the subdirectory.
                        futures.append(executor.submit(scan_directory, entry.path, executor))
                except Exception:
                    # Ignore any entry that cannot be accessed
                    continue
    except Exception:
        return 0, []

    # Process all the subdirectories concurrently.
    for future in futures:
        try:
            sub_total, sub_items = future.result()
            total += sub_total
            items.extend(sub_items)
        except Exception:
            continue

    # Record the size of the directory itself.
    items.append((path, total, "dir"))
    return total, items

def main():
    home_dir = os.path.expanduser("~")
    
    # Use a ThreadPoolExecutor to scan directories concurrently.
    # Adjust max_workers as needed (defaulting here to 16).
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        total_size, all_items = scan_directory(home_dir, executor)
    
    # Sort items by size in descending order.
    sorted_items = sorted(all_items, key=lambda x: x[1], reverse=True)
    
    # Print header.
    print(f"{'Size':>10} {'Type':>4}  Path")
    print("-" * 80)
    
    # Print the top 20 largest items.
    for item in sorted_items[:20]:
        path, size, typ = item
        print(f"{human_readable_size(size):>10} {typ:>4}  {path}")

if __name__ == "__main__":
    main()
