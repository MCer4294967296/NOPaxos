#!/usr/bin/python3
import subprocess, time

mode = input("mode: ")
indices = input("start:end: ").split(":")
if len(indices) == 1:
    indices = range(int(indices[0]))
else:
    indices = range(int(indices[0]), int(indices[1]))

processes = []
for i in indices:
    stderr = subprocess.DEVNULL
    if i == 0:
        stderr = subprocess.STDOUT
    processes.append(subprocess.Popen(["./bench/replica", "-c", "config", "-i", str(i), "-m", mode], stderr=stderr))

input("--Running-- (hit Enter to terminate)")

print("--Killing--")
for process in processes:
    process.terminate()