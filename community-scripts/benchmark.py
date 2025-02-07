#!/usr/bin/env python3
# /// script
# command = "benchmark"
# description = "Benchmark a given URL using ApacheBench"
# aliases = ["benchmark", "ab-benchmark"]
# author = "janoelze"
# dependencies = []
# ///

import sys
import subprocess

def main():
    if len(sys.argv) != 2:
        print("Usage: benchmark <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    reqs = 100
    conc = 5

    # Run ApacheBench with the given parameters.
    cmd = ["ab", "-n", str(reqs), "-c", str(conc), url]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Benchmark failed: {e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
