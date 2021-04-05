#!/usr/bin/python3
import os, subprocess, sys, time

num_cpucores = 40
mode = "vr"
req_per_thread = 20000
runs = range(1,2)

clean = False
if len(sys.argv) > 1 and sys.argv[1] == "c":
    clean = True

for num_processes in runs:
    print(f"initiating run with {num_processes} processes.")

    subprocess.run(f"rm logoutput/{mode}_{num_processes:02}_*", shell=True, stderr=subprocess.DEVNULL)
    processes = []
    files = []
    for process in range(num_processes):
        f = open(f"logoutput/{mode}_{num_processes:02}_{process:02}", "w")
        files.append(f)
        mask = hex(1 << (process % num_cpucores))
        processes.append(subprocess.Popen(["taskset", mask, "./bench/client", "-c", "config", "-w", "1", "-m", mode, "-n", str(req_per_thread)], stderr=f))

    finished = [0]
    while not all(finished):
        print("checking child processes...")
        finished = [p.poll() is not None for p in processes]
        time.sleep(3)

    [f.close() for f in files]
    subprocess.run(f"cat logoutput/{mode}_{num_processes:02}_* > logoutput/{mode}_{num_processes:02}_all", shell=True)
    
    print("run done.")

    if clean:
        r = open(f"logoutput/{mode}_{num_processes:02}_all", "r")
        w = open(f"logoutput/{mode}_{num_processes:02}_cleaned", "w")
        lines = r.readlines()
        output = []
        for line in lines:
            if line[29:].split(" ")[0] in ["Finish", "LATENCY"]:
                output.append(line[29:])
        w.writelines(output)
        w.close()
        r.close()
        print("cleaned.")

if clean:
    summary = []
    for i in runs:
        filename = f"logoutput/{mode}_{i:02}_cleaned"
        with open(filename) as f:
            lines = f.readlines()
    
        assert len(lines) % 2 == 0
        times = []
        # for line in lines[:len(lines)//2]:
        for line in lines[::2]:
            times.append(float(line[64:].split()[0]))

        throughput = sum([req_per_thread/sec for sec in times])
        avg_time = sum(times) / len(times)
        
        latencies = []
        # for line in lines[len(lines)//2:]:
        for line in lines[1::2]:
            latencies.append(int(line[22:].split()[0]))
        avg_latency = sum(latencies) / len(latencies)
        s = "\t".join([mode, str(i), f"{throughput:.3f}", f"{avg_latency:.3f}", str(len(lines) // 2 * req_per_thread), f"{avg_time:.3f}"])
        summary.append(s+"\n")
        print(s)

    f = open("summary", "a")
    f.writelines(summary)
    f.close()
