#!/usr/bin/python3
import subprocess, time

mode = input("mode: ")
indices = input("start:end").split(":")
if len(indices) == 1:
    indices = range(indices[0])
else:
    indices = range(indices[0], indices[1])

processes = []
for i in indices:
    stderr = subprocess.DEVNULL
    if i == 0:
        stderr = subprocess.STDOUT
    processes.append(subprocess.Popen(["./bench/replica", "-c", "config", "-i", str(i), "-m", mode], stderr=stderr))

print("--Running--")
