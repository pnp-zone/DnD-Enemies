#!/usr/bin/env python3

from sys import argv
from collections import defaultdict


if __name__ == "__main__":
    count = defaultdict(int)
    for arg in argv[1:]:
        count[arg] += 1

    for key, value in count.items():
        print(f"{key}: {value}")
