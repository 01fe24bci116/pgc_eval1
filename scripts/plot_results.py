import csv
import matplotlib.pyplot as plt

input_file = "results/benchmark.csv"

rows = []

with open(input_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["DatasetSize"] = int(row["DatasetSize"])
        row["Threads"] = int(row["Threads"])
        row["AverageTimeMs"] = float(row["AverageTimeMs"])
        rows.append(row)

# -------------------------------------------------
# Graph 1: Execution Time vs Dataset Size
# -------------------------------------------------

dataset_sizes = sorted(set(r["DatasetSize"] for r in rows))
thread_values = [1, 2, 4, 8, 16]

plt.figure(figsize=(10, 6))

for threads in thread_values:
    x = []
    y = []

    for size in dataset_sizes:
        matches = [
            r for r in rows
            if r["DatasetSize"] == size
            and r["Threads"] == threads
            and r["Type"] == "OpenMP"
        ]

        if matches:
            x.append(size / 1_000_000)
            y.append(matches[0]["AverageTimeMs"])

    plt.plot(x, y, marker="o", label=f"{threads} Threads")

sequential = [
    r for r in rows
    if r["Type"] == "Sequential"
]

x = [r["DatasetSize"] / 1_000_000 for r in sequential]
y = [r["AverageTimeMs"] for r in sequential]

plt.plot(x, y, marker="o", linewidth=2, label="Sequential")

plt.xlabel("Dataset Size (Millions of Elements)")
plt.ylabel("Execution Time (ms)")
plt.title("Execution Time vs Dataset Size")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/execution_time_vs_dataset.png", dpi=300)
plt.close()


# -------------------------------------------------
# Graph 2: Execution Time vs Number of Threads
# -------------------------------------------------

plt.figure(figsize=(10, 6))

selected_sizes = [10_000_000, 50_000_000, 100_000_000, 200_000_000]

for size in selected_sizes:

    x = []
    y = []

    for threads in thread_values:

        matches = [
            r for r in rows
            if r["DatasetSize"] == size
            and r["Threads"] == threads
            and r["Type"] == "OpenMP"
        ]

        if matches:
            x.append(threads)
            y.append(matches[0]["AverageTimeMs"])

    plt.plot(x, y, marker="o", label=f"{size // 1_000_000}M Elements")

plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (ms)")
plt.title("OpenMP Execution Time vs Number of Threads")
plt.xticks(thread_values)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/thread_scaling.png", dpi=300)
plt.close()


# -------------------------------------------------
# Graph 3: Speedup vs Number of Threads
# -------------------------------------------------

plt.figure(figsize=(10, 6))

for size in selected_sizes:

    sequential_matches = [
        r for r in rows
        if r["DatasetSize"] == size
        and r["Type"] == "Sequential"
    ]

    if not sequential_matches:
        continue

    sequential_time = sequential_matches[0]["AverageTimeMs"]

    x = []
    y = []

    for threads in thread_values:

        matches = [
            r for r in rows
            if r["DatasetSize"] == size
            and r["Threads"] == threads
            and r["Type"] == "OpenMP"
        ]

        if matches:
            speedup = sequential_time / matches[0]["AverageTimeMs"]
            x.append(threads)
            y.append(speedup)

    plt.plot(x, y, marker="o", label=f"{size // 1_000_000}M Elements")

plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.title("OpenMP Speedup vs Number of Threads")
plt.xticks(thread_values)
plt.axhline(y=1, linestyle="--", linewidth=1)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/speedup_vs_threads.png", dpi=300)
plt.close()


# -------------------------------------------------
# Graph 4: Parallel Efficiency
# -------------------------------------------------

plt.figure(figsize=(10, 6))

for size in selected_sizes:

    sequential_matches = [
        r for r in rows
        if r["DatasetSize"] == size
        and r["Type"] == "Sequential"
    ]

    if not sequential_matches:
        continue

    sequential_time = sequential_matches[0]["AverageTimeMs"]

    x = []
    y = []

    for threads in thread_values:

        matches = [
            r for r in rows
            if r["DatasetSize"] == size
            and r["Threads"] == threads
            and r["Type"] == "OpenMP"
        ]

        if matches:
            speedup = sequential_time / matches[0]["AverageTimeMs"]
            efficiency = (speedup / threads) * 100

            x.append(threads)
            y.append(efficiency)

    plt.plot(x, y, marker="o", label=f"{size // 1_000_000}M Elements")

plt.xlabel("Number of Threads")
plt.ylabel("Parallel Efficiency (%)")
plt.title("OpenMP Parallel Efficiency")
plt.xticks(thread_values)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/parallel_efficiency.png", dpi=300)
plt.close()

print("============================================")
print(" Graph generation completed successfully")
print("============================================")
print("Created:")
print("  graphs/execution_time_vs_dataset.png")
print("  graphs/thread_scaling.png")
print("  graphs/speedup_vs_threads.png")
print("  graphs/parallel_efficiency.png")
print("============================================")
