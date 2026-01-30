import os
import random
import subprocess
import time
import csv
import matplotlib.pyplot as plt


DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)


NS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]


MATCHER = "src\\matcher.py"
VERIFIER = "src\\verifier.py"


CSV_FILE = os.path.join(DATA_FOLDER, "scalability.csv")


def generate_input(n, file_path):
    with open(file_path, "w") as f:
        f.write(f"{n}\n")

        for _ in range(n):
            perm = list(range(1, n+1))
            random.shuffle(perm)
            f.write(" ".join(map(str, perm)) + "\n")

        for _ in range(n):
            perm = list(range(1, n+1))
            random.shuffle(perm)
            f.write(" ".join(map(str, perm)) + "\n")


def main():
    results = []

    for n in NS:
        file_in = os.path.join(DATA_FOLDER, f"random{n}.in")
        print(f"Generating input for n={n} ...")
        generate_input(n, file_in)


        start = time.time()
        subprocess.run(f"python {MATCHER} < {file_in}", shell=True)
        matcher_time = time.time() - start

        start = time.time()
        subprocess.run(f"python {MATCHER} < {file_in} | python {VERIFIER} {file_in}", shell=True)
        total_time = time.time() - start

        print(f"n={n} → matcher: {matcher_time:.5f}s, matcher+verifier: {total_time:.5f}s\n")
        results.append((n, matcher_time, total_time))


    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "matcher_time", "matcher_plus_verifier_time"])
        writer.writerows(results)


    plot_graph(results)

def plot_graph(results):
    ns, matcher_times, total_times = zip(*results)
    plt.plot(ns, matcher_times, marker="o", label="Matcher")
    plt.plot(ns, total_times, marker="x", label="Matcher + Verifier")
    plt.xlabel("Number of Hospitals/Students (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Scalability of Gale-Shapley Matcher & Verifier")
    plt.grid(True)
    plt.legend()
    plt.xscale("log", base=2)  
    plt.yscale("log")
    plt.savefig(os.path.join(DATA_FOLDER, "scalability_graph.png"))
    plt.show()


if __name__ == "__main__":
    main()
