#!/usr/bin/env python3
# /// script
# command = "currenttime"
# description = "Print the current time"
# aliases = ["currenttime"]
# author = "janoelze"
# dependencies = []
# ///

import os

def main():
    print("Current time:")
    os.system("date")

if __name__ == "__main__":
    main()